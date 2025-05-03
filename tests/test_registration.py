import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestUserRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Update with your server URL
        cls.driver.get(cls.base_url + "/registration.html")

    def test_successful_registration(self):
        """Scenario: Successful user registration"""
        driver = self.driver
        
        # Fill in valid registration details
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm-password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify success message
        success_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "registration-success"))
        )
        self.assertIn("Registration successful", success_message.text)
        
        # Verify redirection to products page
        WebDriverWait(driver, 5).until(
            EC.url_contains("products.html")
        )

    def test_username_validation(self):
        """Scenario: Registration with invalid username"""
        driver = self.driver
        driver.get(self.base_url + "/registration.html")
        
        # Fill in form with short username
        driver.find_element(By.ID, "username").send_keys("abc")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm-password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify error message
        error_message = driver.find_element(By.ID, "username-error")
        self.assertIn("must be at least 4 characters", error_message.text)

    def test_password_mismatch(self):
        """Scenario: Registration with password mismatch"""
        driver = self.driver
        driver.get(self.base_url + "/registration.html")
        
        # Fill in form with mismatched passwords
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm-password").send_keys("different")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify error message
        error_message = driver.find_element(By.ID, "confirm-password-error")
        self.assertIn("Passwords do not match", error_message.text)

    def test_invalid_email(self):
        """Scenario: Registration with invalid email"""
        driver = self.driver
        driver.get(self.base_url + "/registration.html")
        
        # Fill in form with invalid email
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("invalid-email")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm-password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify error message
        error_message = driver.find_element(By.ID, "email-error")
        self.assertIn("valid email address", error_message.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()