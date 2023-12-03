import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LoginTest(unittest.TestCase):
    def setUp(self):
        # Start the Selenium WebDriver
        self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
        self.driver.get('http://127.0.0.1:3000/login/') # Replace with the actual URL of your login page

    def test_login_successful(self):
        # Find the username, password, and login button elements
        email_input = self.driver.find_element(By.NAME, 'email')  # Use By.NAME for the name attribute
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")

        # Enter valid credentials
        email_input.send_keys("Sanjo31@gmail.com")
        password_input.send_keys("Sanjo@31")

        # Click the login button
        login_button.click()

        # Wait for a while to see the result (you can adjust this based on your application's response time)
        time.sleep(2)
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/home/')
    
    def tearDown(self):
        # Close the browser window
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
