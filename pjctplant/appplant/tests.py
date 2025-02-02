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
#         email_input.send_keys("nimmysibi25@gmail.com")
#         password_input.send_keys("Nimmy@31")

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


######addproduct####################################################################################################

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
    


#####Search product#######################################################################################################

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# class LoginAndSearchTest(unittest.TestCase):
#     def setUp(self):
#         # Start the Selenium WebDriver
#         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
#         self.driver.get('http://127.0.0.1:3000/login/')  # Replace with the actual URL of your login page

#     def test_login_and_search_successful(self):
#         # Find the username, password, and login button elements for the login page
#         email_input = self.driver.find_element(By.NAME, 'email')  # Use By.NAME for the name attribute
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")

#         # Enter valid credentials and click login
#         email_input.send_keys("nimmysibi25@gmail.com")
#         password_input.send_keys("Nimmy@31")
#         login_button.click()

#         # Wait for a while to ensure the login process completes (you can adjust this based on your application's response time)
#         time.sleep(2)

#         # Assert that the login was successful by checking the current URL
#         self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/home/')  # Corrected URL for home page

#         # Now, navigate to the product search page
#         self.driver.get('http://127.0.0.1:3000/subcategory/flowering-plants/')

#         # Find the search input field and enter the search term 'jasmin'
#         search_input = self.driver.find_element(By.CLASS_NAME, 'search-input')
#         search_input.send_keys('jasmin')

#         # Submit the search form
#         search_input.submit()

#         # Wait for a while to see the result (you can adjust this based on your application's response time)
#         time.sleep(2)

#         # Now, you can perform additional assertions based on the search results or other criteria

#     def tearDown(self):
#         # Close the browser window
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()

###################################################### add to cart####################################
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# class LoginAndAddToCartTest(unittest.TestCase):
#     def setUp(self):
#         # Start the Selenium WebDriver
#         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
#         self.driver.get('http://127.0.0.1:3000/login/')  # Replace with the actual URL of your login page

#     def test_login_add_to_cart_and_view_cart(self):
#         # Find the username, password, and login button elements for the login page
#         email_input = self.driver.find_element(By.NAME, 'email')  # Use By.NAME for the name attribute
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")

#         # Enter valid credentials and click login
#         email_input.send_keys("nimmysibi25@gmail.com")
#         password_input.send_keys("Nimmy@31")
#         login_button.click()

#         # Wait for a while to ensure the login process completes (you can adjust this based on your application's response time)
#         time.sleep(2)

#         # Now, navigate to the product search page
#         self.driver.get('http://127.0.0.1:3000/subcategory/flowering-plants/')

#         # Find the 'Add to Cart' button and click it
#         add_to_cart_button = self.driver.find_element(By.XPATH, "//button[text()='Add to Cart']")
#         add_to_cart_button.click()

#         # Wait for a while to ensure the product is added to the cart (you can adjust this based on your application's response time)
#         time.sleep(2)

#         # Now, navigate to the view cart page
#         self.driver.get('http://127.0.0.1:3000/view_cart/')

#         # Wait for a while to see the result (you can adjust this based on your application's response time)
#         time.sleep(2)

#         # Now, you can perform additional assertions based on the content of the view cart page

#     def tearDown(self):
#         # Close the browser window
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()

#########################################################################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Start Chrome WebDriver
# driver = webdriver.Chrome()

# # Set the maximum wait time (in seconds) for Selenium actions
# driver.implicitly_wait(10)  # Implicit wait for elements to be present

# # Open the login page
# driver.get("http://127.0.0.1:3000/login/")

# # Find and fill in the email and password fields
# email_input = driver.find_element(By.ID, "email")
# password_input = driver.find_element(By.ID, "password")

# email_input.send_keys("drbenjamin1@gmail.com")
# password_input.send_keys("Sanjo@1010")

# # Click the login button
# login_button = driver.find_element(By.CSS_SELECTOR, ".login-button")
# login_button.click()

# # Navigate to the dashboard page
# driver.get("http://127.0.0.1:3000/consult/")

# # Wait for the scheduling link to be clickable
# scheduling_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Scheduling")))
# scheduling_link.click()

# # Now you are on the scheduling page
# # Perform any further actions on this page as needed

# # Close the WebDriver session
# driver.quit()
# #########################################################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Start Chrome WebDriver
# driver = webdriver.Chrome()

# # Set the maximum wait time (in seconds) for Selenium actions
# driver.implicitly_wait(5)  # Implicit wait for elements to be present

# # Open the dashboard page
# driver.get("http://127.0.0.1:3000/consult/")

# # Wait for the scheduling button to be clickable
# try:
#     scheduling_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Scheduling")))
#     scheduling_button.click()

#     # Wait for the redirect to the appointment page with increased timeout
#     WebDriverWait(driver, 30).until(EC.url_to_be("http://127.0.0.1:3000/appoint/"))

#     # Now you are on the appointment page
#     # Perform any further actions on this page as needed

#     print("Successfully redirected to http://127.0.0.1:3000/appoint/")
    
# except Exception as e:
#     print("An error occurred:", e)

# finally:
#     # Close the WebDriver session
#     driver.quit()



#####################################################################################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# try:
#     # Start Chrome WebDriver
#     driver = webdriver.Chrome()

#     # Set the maximum wait time (in seconds) for Selenium actions
#     driver.implicitly_wait(20)  # Implicit wait for elements to be present

#     # Open the dashboard page
#     driver.get("http://127.0.0.1:3000/consult/")

#     # Wait for the scheduling button to be clickable
#     scheduling_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Scheduling")))
#     scheduling_button.click()

#     # Wait for the redirect to the appointment page with increased timeout
#     # WebDriverWait(driver, 60).until(EC.url_to_be("http://127.0.0.1:3000/appoint/"))
#     driver.get("http://127.0.0.1:3000/appoint/")


#     # Now you are on the appointment page
#     # Perform any further actions on this page as needed

#     print("Successfully redirected to http://127.0.0.1:3000/appoint/")

# except Exception as e:
#     print("An error occurred:", e)

# finally:
#     # Close the WebDriver session
#     driver.quit()


#################################################
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# try:
#     # Start Chrome WebDriver
#     driver = webdriver.Chrome()

#     # Set the maximum wait time (in seconds) for Selenium actions
#     driver.implicitly_wait(20)  # Implicit wait for elements to be present

#     # Open the login page
#     driver.get("http://127.0.0.1:3000/login/")

#     # Find and fill in the email and password fields
#     email_input = driver.find_element(By.ID, "email")
#     email_input.send_keys("nimmysibi25@gmail.com")

#     password_input = driver.find_element(By.ID, "password")
#     password_input.send_keys("Nimmy@31")

#     # Find and click the login button
#     login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#     login_button.click()

#     # Wait for the redirect to the home page
#     WebDriverWait(driver, 20).until(EC.url_to_be("http://127.0.0.1:3000/home/"))

#     print("Successfully logged in and redirected to the home page")

# except Exception as e:
#     print("An error occurred:", e)

# finally:
#     # Close the WebDriver session
#     driver.quit()

#####################################################################3

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

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
#         email_input.send_keys("nimmysibi25@gmail.com")
#         password_input.send_keys("Nimmy@31")

#         # Click the login button
#         login_button.click()

#         # Wait for the home page to load
#         WebDriverWait(self.driver, 10).until(EC.url_contains("http://127.0.0.1:3000/botanist_list/"))

#         # Assert that the current URL is 'http://127.0.0.1:3000/botanist_list/'
#         self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/botanist_list/')

#     def tearDown(self):
#         # Close the browser window
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()



################################################################
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LoginAndAddToCartTest(unittest.TestCase):
     def setUp(self):
         # Start the Selenium WebDriver
         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
         self.driver.get('http://127.0.0.1:3000/login/')  # Replace with the actual URL of your login page

     def test_login_add_to_cart_and_view_cart(self):
         # Find the username, password, and login button elements for the login page
         email_input = self.driver.find_element(By.NAME, 'email')  # Use By.NAME for the name attribute
         password_input = self.driver.find_element(By.NAME, 'password')
         login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")

         # Enter valid credentials and click login
         email_input.send_keys("nimmysibi25@gmail.com")
         password_input.send_keys("Nimmy@31")
         login_button.click()

         # Wait for a while to ensure the login process completes (you can adjust this based on your application's response time)
         time.sleep(2)

         # Now, navigate to the product search page
         self.driver.get('http://127.0.0.1:3000/botanist_list/')

         # Find the 'Add to Cart' button and click it
         book_now_button = self.driver.find_element(By.XPATH, "//button[text()='Book now']")
         book_now_button.click()

         # Wait for a while to ensure the product is added to the cart (you can adjust this based on your application's response time)
         time.sleep(2)

         # Now, navigate to the view cart page
         self.driver.get('http://127.0.0.1:3000/book-appointment/54/')

         # Wait for a while to see the result (you can adjust this based on your application's response time)
         time.sleep(2)

         # Now, you can perform additional assertions based on the content of the view cart page

     def tearDown(self):
         # Close the browser window
         self.driver.close()

if __name__ == "__main__":
     unittest.main()


