from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Firefox()
    
    def tearDown(self):
        self.brower.quit()
    
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

        table = self.brower.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )

        # The page shows textbar again which can input other To-Dos
        # She typed "Use peacock feathers to make a fly"
        self.fail('Finish the test!')

        # The page updates again and shows two To-Dos

if __name__ == "__main__":
    unittest.main(warnings='ignore')

