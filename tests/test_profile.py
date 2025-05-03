import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestUserProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Update with your server URL
        
        # Register a test user first
        cls.driver.get(cls.base_url + "/registration.html")
        cls.driver.find_element(By.ID, "username").send_keys("profiletest")
        cls.driver.find_element(By.ID, "email").send_keys("profiletest@example.com")
        cls.driver.find_element(By.ID, "password").send_keys("password123")
        cls.driver.find_element(By.ID, "confirm-password").send_keys("password123")
        cls.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for registration to complete
        WebDriverWait(cls.driver, 5).until(
            EC.url_contains("products.html")
        )
        
        # Go to profile page
        cls.driver.get(cls.base_url + "/profile.html")

    def test_update_profile_information(self):
        """Scenario: Updating profile information successfully"""
        driver = self.driver
        
        # Fill in profile form
        driver.find_element(By.ID, "full-name").send_keys("Test User")
        driver.find_element(By.ID, "address").send_keys("123 Test Street, Test City")
        driver.find_element(By.ID, "phone").send_keys("555-123-4567")
        driver.find_element(By.CSS_SELECTOR, "#profileForm button[type='submit']").click()
        
        # Verify success message
        success_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile-update-result .success-message"))
        )
        self.assertIn("Profile updated successfully", success_message.text)
        
        # Refresh page and verify persistence
        driver.refresh()
        self.assertEqual(driver.find_element(By.ID, "full-name").get_attribute("value"), "Test User")
        self.assertEqual(driver.find_element(By.ID, "address").get_attribute("value"), "123 Test Street, Test City")
        self.assertEqual(driver.find_element(By.ID, "phone").get_attribute("value"), "555-123-4567")

    def test_change_password_successfully(self):
        """Scenario: Changing password successfully"""
        driver = self.driver
        
        # Switch to change password tab
        driver.find_element(By.XPATH, "//button[contains(text(), 'Change Password')]").click()
        
        # Fill in password form
        driver.find_element(By.ID, "current-password").send_keys("password123")
        driver.find_element(By.ID, "new-password").send_keys("newpassword123")
        driver.find_element(By.ID, "confirm-new-password").send_keys("newpassword123")
        driver.find_element(By.CSS_SELECTOR, "#passwordForm button[type='submit']").click()
        
        # Verify success message
        success_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#password-change-result .success-message"))
        )
        self.assertIn("Password changed successfully", success_message.text)

    def test_change_password_mismatch(self):
        """Scenario: Attempting to change password with mismatched new passwords"""
        driver = self.driver
        
        # Switch to change password tab if not already there
        if not driver.find_element(By.ID, "change-password").is_displayed():
            driver.find_element(By.XPATH, "//button[contains(text(), 'Change Password')]").click()
        
        # Fill in password form with mismatch
        driver.find_element(By.ID, "current-password").send_keys("password123")
        driver.find_element(By.ID, "new-password").send_keys("newpassword123")
        driver.find_element(By.ID, "confirm-new-password").send_keys("differentpassword")
        driver.find_element(By.CSS_SELECTOR, "#passwordForm button[type='submit']").click()
        
        # Verify error message
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "confirm-new-password-error"))
        )
        self.assertIn("Passwords do not match", error_message.text)

    def test_change_password_short_new_password(self):
        """Scenario: Attempting to change password with too short new password"""
        driver = self.driver
        
        # Switch to change password tab if not already there
        if not driver.find_element(By.ID, "change-password").is_displayed():
            driver.find_element(By.XPATH, "//button[contains(text(), 'Change Password')]").click()
        
        # Fill in password form with short password
        driver.find_element(By.ID, "current-password").send_keys("password123")
        driver.find_element(By.ID, "new-password").send_keys("short")
        driver.find_element(By.ID, "confirm-new-password").send_keys("short")
        driver.find_element(By.CSS_SELECTOR, "#passwordForm button[type='submit']").click()
        
        # Verify error message
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "new-password-error"))
        )
        self.assertIn("must be at least 6 characters", error_message.text)

    def test_profile_tab_switching(self):
        """Scenario: Switching between profile information and change password tabs"""
        driver = self.driver
        
        # Start on profile info tab (default)
        self.assertTrue(driver.find_element(By.ID, "profile-info").is_displayed())
        self.assertFalse(driver.find_element(By.ID, "change-password").is_displayed())
        
        # Click change password tab
        driver.find_element(By.XPATH, "//button[contains(text(), 'Change Password')]").click()
        
        # Verify tabs switched
        self.assertFalse(driver.find_element(By.ID, "profile-info").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "change-password").is_displayed())
        
        # Click back to profile info tab
        driver.find_element(By.XPATH, "//button[contains(text(), 'Profile Information')]").click()
        
        # Verify tabs switched back
        self.assertTrue(driver.find_element(By.ID, "profile-info").is_displayed())
        self.assertFalse(driver.find_element(By.ID, "change-password").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()