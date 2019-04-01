from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Firefox()
    
    def tearDown(self):
        self.brower.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.brower.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice visits the website
        self.brower.get('http://localhost:8000')

        # Title and Header includes 'To-Do'
        self.assertIn('To-Do', self.brower.title)
        header_text = self.brower.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The web app invites her to a To-Do event
        inputbox = self.brower.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She typed into a input bar the words: 'Buy peacock feathers'
        inputbox.send_keys('Buy peacock feathers')

        # The page updated when she pressed Enter
        # The To-Do lists shows: '1. Buy peacock feathers'
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # The page shows textbar again which can input other To-Dos
        # She typed "Use peacock feathers to make a fly"
        inputbox = self.brower.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The Page updates again, the lists shows two events
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Make peacock feathers to make a fly')
        # She wants find out wheather this site can remember her lists
        # She saw this site generates an unique url for her
        # And the site has some texts to explain the function
        self.fail('Finish the test!')

        # She visits the site and the lists are there

if __name__ == "__main__":
    unittest.main(warnings='ignore')

