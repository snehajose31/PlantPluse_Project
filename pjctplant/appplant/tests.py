# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# class LoginTest(unittest.TestCase):
#     def setUp(self):
#         # Start the Selenium WebDriver
#         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
#         self.driver.get('http://127.0.0.1:3000/login/') # Replace with the actual URL of your login page

#     def test_login_successful(self):
#         # Find the username, password, and login button elements
#         email_input = self.driver.find_element(By.NAME, 'email')  # Use By.NAME for the name attribute
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")

#         # Enter valid credentials
#         email_input.send_keys("Sanjo31@gmail.com")
#         password_input.send_keys("Sanjo@31")

#         # Click the login button
#         login_button.click()

#         # Wait for a while to see the result (you can adjust this based on your application's response time)
#         time.sleep(2)
#         self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/home/')
    
#     def tearDown(self):
#         # Close the browser window
#         self.driver.close()

# if __name__ == "_main_":
#     unittest.main()


######addproduct
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# class AddProductTest(unittest.TestCase):
#     def setUp(self):
#         # Start the Selenium WebDriver
#         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
#         self.driver.get('http://127.0.0.1:3000/addproduct/')  # Replace with the actual URL of your add product page

#     def test_add_product(self):
#         # Find the form inputs and submit button
#         product_name_input = self.driver.find_element(By.ID, 'product-name')
#         category_dropdown = self.driver.find_element(By.ID, 'category-name')
#         subcategory_dropdown = self.driver.find_element(By.ID, 'subcategory-name')
#         stock_input = self.driver.find_element(By.ID, 'stock')
#         description_input = self.driver.find_element(By.ID, 'description')
#         price_input = self.driver.find_element(By.ID, 'price')
#         discount_input = self.driver.find_element(By.ID, 'discount')
#         status_dropdown = self.driver.find_element(By.ID, 'status')
#         image_input = self.driver.find_element(By.ID, 'product-image')
#         add_product_button = self.driver.find_element(By.ID, 'add-product-button')

#         # Enter valid product details
#         product_name_input.send_keys("Test Product")
#         category_dropdown.send_keys("plant")  # Change based on your category
#         subcategory_dropdown.send_keys("flowering plant")  # Change based on your subcategory
#         stock_input.send_keys("10")
#         description_input.send_keys("This is a test product description.")
#         price_input.send_keys("100")
#         discount_input.send_keys("10")
#         status_dropdown.send_keys("active")  # Change based on your status
#         image_input.send_keys(r"C:\Users\DELL\Desktop\pulse\pjctplant\static\images\bck10.jpg")  # Replace with the actual path to your test image

#         # Submit the form
#         add_product_button.click()

#         # Open the view product page
#         self.driver.get("http://127.0.0.1:3000/viewproduct/")  # Change the URL accordingly

        
#     def tearDown(self):
#         # Close the browser window
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()
    
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTest(TestCase):
    def setUp(self):
        # Set up the WebDriver in the setUp method
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Close the WebDriver in the tearDown method
        self.driver.quit()

    def test_add_to_cart_and_redirect_to_view_cart(self):
        # Navigate to the Flowering Plants page
        self.driver.get('http://127.0.0.1:3000/subcategory/flowering-plants/')  # Update the URL as needed

        # Wait for the 'Add to Cart' button on the product page
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'add-to-cart-btn'))
        )
        print("Found 'Add to Cart' button")

        # Click on the "Add to Cart" button
        add_to_cart_button.click()
        print("Clicked on 'Add to Cart' button")

        # Wait for the confirmation message on the View Cart page
        confirmation_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'confirmation-message'))
        )
        print(f"Confirmation message: {confirmation_message.text}")

        # Check if the URL is redirected to the view cart page
        current_url = self.driver.current_url
        self.assertTrue(current_url.endswith('/view_cart/'))

        # Add assertions to check if the product was added to the cart successfully
        # For example, check if the confirmation message is displayed
        self.assertIn('successfully added to your cart', confirmation_message.text.lower())
