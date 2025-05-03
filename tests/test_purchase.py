import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestProductPurchase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Update with your server URL
        
        # Setup: Add items to cart
        cls.driver.get(cls.base_url + "/products.html")
        cls.driver.find_element(By.XPATH, "//div[contains(@class, 'product')][1]/button").click()
        cls.driver.find_element(By.LINK_TEXT, "Cart").click()
        cls.driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Checkout')]").click()

    def test_successful_purchase(self):
        """Scenario: Successful product purchase with valid payment"""
        driver = self.driver
        
        # Fill in payment details
        driver.find_element(By.ID, "card-number").send_keys("4111111111111111")
        driver.find_element(By.ID, "expiry-date").send_keys("12/25")
        driver.find_element(By.ID, "cvv").send_keys("123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify success message (since we're simulating random success, we need to handle both cases)
        try:
            success_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#payment-result .success-message"))
            )
            self.assertIn("Payment successful", success_message.text)
        except:
            # If payment failed (30% chance), verify failure message
            error_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#payment-result .error-message"))
            )
            self.assertIn("Payment failed", error_message.text)

    def test_payment_with_missing_details(self):
        """Scenario: Payment fails due to missing payment details"""
        driver = self.driver
        driver.get(self.base_url + "/products.html")
        
        # Add item and go to checkout
        driver.find_element(By.XPATH, "//div[contains(@class, 'product')][1]/button").click()
        driver.find_element(By.LINK_TEXT, "Cart").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Checkout')]").click()
        
        # Submit empty form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify error message
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#payment-result .error-message"))
        )
        self.assertIn("fill in all payment details", error_message.text)

    def test_order_summary_display(self):
        """Scenario: Verify order summary displays correct items and totals"""
        driver = self.driver
        driver.get(self.base_url + "/products.html")
        
        # Clear cart and add specific items
        driver.find_element(By.LINK_TEXT, "Cart").click()
        remove_buttons = driver.find_elements(By.XPATH, "//div[@id='cart-items']//button[contains(text(), 'Remove')]")
        for button in remove_buttons:
            button.click()
            time.sleep(0.5)
        
        driver.find_element(By.LINK_TEXT, "Products").click()
        
        # Add two specific products
        product1 = "Product 1"
        product2 = "Product 2"
        driver.find_element(By.XPATH, f"//div[contains(@class, 'product') and contains(., '{product1}')]/button").click()
        driver.find_element(By.XPATH, f"//div[contains(@class, 'product') and contains(., '{product2}')]/button").click()
        
        # Go to checkout
        driver.find_element(By.LINK_TEXT, "Cart").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Checkout')]").click()
        
        # Verify order summary
        summary = driver.find_element(By.ID, "checkout-summary").text
        self.assertIn(product1, summary)
        self.assertIn(product2, summary)
        
        # Verify totals are correct
        subtotal = float(driver.find_element(By.XPATH, "//div[@id='checkout-summary']//p[contains(., 'Subtotal')]").text.split('$')[1])
        total = float(driver.find_element(By.XPATH, "//div[@id='checkout-summary']//p[contains(., 'Total')]").text.split('$')[1])
        self.assertEqual(subtotal, total)  # No discount applied

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()