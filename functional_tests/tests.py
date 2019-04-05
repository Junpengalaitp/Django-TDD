import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
            
    # def test_can_start_a_list_and_retrieve_it_later(self):
    #     # Alice visits the website
    #     self.browser.get(self.live_server_url)

    #     # Title and Header includes 'To-Do'
    #     self.assertIn('To-Do', self.browser.title)
    #     header_text = self.browser.find_element_by_tag_name('h1').text
    #     self.assertIn('To-Do', header_text)

    #     # The web app invites her to a To-Do event
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     self.assertEqual(
    #         inputbox.get_attribute('placeholder'),
    #         'Enter a to-do item'
    #     )

    #     # She typed into a input bar the words: 'Buy peacock feathers'
    #     inputbox.send_keys('Buy peacock feathers')

    #     # The page updated when she pressed Enter
    #     # The To-Do lists shows: '1. Buy peacock feathers'
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')

    #     # The page shows textbar again which can input other To-Dos
    #     # She typed "Use peacock feathers to make a fly"
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('Make peacock feathers to make a fly')
    #     inputbox.send_keys(Keys.ENTER)

    #     # The Page updates again, the lists shows two events
    #     self.wait_for_row_in_list_table('2: Make peacock feathers to make a fly')
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')
    #     # She wants find out wheather this site can remember her lists
    #     # She saw this site generates an unique url for her
    #     # And the site has some texts to explain the function
        
    #     # self.fail('Finish the test!')

    #     # She visits the site and the lists are there


    def test_can_start_a_list_for_one_user(self):
            # Alice visits the website
            self.browser.get(self.live_server_url)

            # Title and Header includes 'To-Do'
            self.assertIn('To-Do', self.browser.title)
            header_text = self.browser.find_element_by_tag_name('h1').text
            self.assertIn('To-Do', header_text)

            # The web app invites her to a To-Do event
            inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

            # She typed into a input bar the words: 'Buy peacock feathers'
            inputbox.send_keys('Buy peacock feathers')

            # The page updated when she pressed Enter
            # The To-Do lists shows: '1. Buy peacock feathers'
            inputbox.send_keys(Keys.ENTER)
            self.wait_for_row_in_list_table('1: Buy peacock feathers')

            # The page shows textbar again which can input other To-Dos
            # She typed "Use peacock feathers to make a fly"
            inputbox = self.browser.find_element_by_id('id_new_item')
            inputbox.send_keys('Make peacock feathers to make a fly')
            inputbox.send_keys(Keys.ENTER)

            # The Page updates again, the lists shows two events
            self.wait_for_row_in_list_table('2: Make peacock feathers to make a fly')
            self.wait_for_row_in_list_table('1: Buy peacock feathers')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Alice creates a new To-do lists
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She noticed a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        
        # Now a new user Frank visits the site

        ## We start a new browser session
        ## Make sure Alice's information does not leak from cookie
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Frank visits the main page
        # The page does not show Alice's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Frank enters a new To-Do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Frank got his unique URL
        frank_list_url = self.browser.current_url
        self.assertRegex(frank_list_url, '/lists/.+')
        self.assertNotEqual(frank_list_url, edith_list_url)

        # This page still does not show Alice's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        # Alice visits home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She saw the input box diplayed in the middle
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She create a new list and the inputbox still displayed in the middle
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )