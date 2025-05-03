import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestShoppingCart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Update with your server URL
        cls.driver.get(cls.base_url + "/products.html")

    def test_add_item_to_cart(self):
        """Scenario: Adding an item to the shopping cart"""
        driver = self.driver
        
        # Add first product to cart
        product_name = "Product 1"
        add_button = driver.find_element(By.XPATH, f"//div[contains(@class, 'product') and contains(., '{product_name}')]/button")
        add_button.click()
        
        # Verify cart count updates
        cart_count = WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "cart-count"), "1")
        )
        
        # Go to cart page
        driver.find_element(By.LINK_TEXT, "Cart").click()
        
        # Verify item is in cart
        cart_item = driver.find_element(By.XPATH, f"//div[@id='cart-items']//h3[contains(text(), '{product_name}')]")
        self.assertTrue(cart_item.is_displayed())

    def test_remove_item_from_cart(self):
        """Scenario: Removing an item from the shopping cart"""
        driver = self.driver
        driver.get(self.base_url + "/products.html")
        
        # Add two products to cart
        driver.find_element(By.XPATH, "//div[contains(@class, 'product')][1]/button").click()
        driver.find_element(By.XPATH, "//div[contains(@class, 'product')][2]/button").click()
        
        # Go to cart page
        driver.find_element(By.LINK_TEXT, "Cart").click()
        
        # Remove first item
        remove_buttons = driver.find_elements(By.XPATH, "//div[@id='cart-items']//button[contains(text(), 'Remove')]")
        remove_buttons[0].click()
        
        # Verify only one item remains
        cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
        self.assertEqual(len(cart_items), 1)

    def test_apply_valid_discount(self):
        """Scenario: Applying a valid discount code"""
        driver = self.driver
        driver.get(self.base_url + "/products.html")
        
        # Add a product to cart
        driver.find_element(By.XPATH, "//div[contains(@class, 'product')][1]/button").click()
        
        # Go to cart page
        driver.find_element(By.LINK_TEXT, "Cart").click()
        
        # Get initial total
        initial_total = float(driver.find_element(By.ID, "total").text)
        
        # Apply valid discount
        discount_input = driver.find_element(By.ID, "discount-code")
        discount_input.send_keys("DISCOUNT10")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()
        
        # Verify discount applied
        discount_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "discount-message"))
        )
        self.assertIn("10% discount applied", discount_message.text)
        
        # Verify total is reduced by 10%
        discounted_total = float(driver.find_element(By.ID, "total").text)
        self.assertAlmostEqual(discounted_total, initial_total * 0.9, places=2)

    def test_apply_invalid_discount(self):
        """Scenario: Applying an invalid discount code"""
        driver = self.driver
        driver.get(self.base_url + "/products.html")
        
        # Add a product to cart
        driver.find_element(By.XPATH, "//div[contains(@class, 'product')][1]/button").click()
        
        # Go to cart page
        driver.find_element(By.LINK_TEXT, "Cart").click()
        
        # Get initial total
        initial_total = float(driver.find_element(By.ID, "total").text)
        
        # Apply invalid discount
        discount_input = driver.find_element(By.ID, "discount-code")
        discount_input.send_keys("INVALIDCODE")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()
        
        # Verify error message
        discount_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "discount-message"))
        )
        self.assertIn("Invalid discount code", discount_message.text)
        
        # Verify total remains unchanged
        current_total = float(driver.find_element(By.ID, "total").text)
        self.assertEqual(current_total, initial_total)

    def test_proceed_to_checkout_with_empty_cart(self):
        """Scenario: Attempting to checkout with an empty cart"""
        driver = self.driver
        driver.get(self.base_url + "/cart.html")
        
        # Clear cart if needed
        remove_buttons = driver.find_elements(By.XPATH, "//div[@id='cart-items']//button[contains(text(), 'Remove')]")
        for button in remove_buttons:
            button.click()
            time.sleep(0.5)  # Allow time for removal
        
        # Click checkout button
        driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Checkout')]").click()
        
        # Verify alert appears
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        self.assertIn("empty", alert.text)
        alert.accept()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()