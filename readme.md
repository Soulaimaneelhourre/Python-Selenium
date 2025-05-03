# Mini E-Commerce Application

A complete mini e-commerce application with user registration, shopping cart, product purchase, and profile management features. Includes BDD scenarios and Selenium tests.

## Features

1. **User Registration**
   - New user signup with validation
   - Form validation for username, email, and password
   - Success/failure messaging

2. **Shopping Cart**
   - Add/remove products
   - Quantity management
   - Discount code application
   - Cart persistence

3. **Product Purchase**
   - Checkout process
   - Payment form
   - Order summary
   - Success/failure handling

4. **User Profile Management**
   - Profile information editing
   - Password change functionality
   - Tab-based interface

## Project Structure
ecommerce-mini-project/
│
├── index.html # Main page
├── registration.html # User registration page
├── profile.html # User profile page
├── products.html # Product listing page
├── cart.html # Shopping cart page
├── checkout.html # Checkout page
├── css/
│ └── style.css # Stylesheet
├── js/
│ └── script.js # Main JavaScript
├── tests/
│ ├── test_registration.py # Registration tests
│ ├── test_cart.py # Shopping cart tests
│ ├── test_purchase.py # Purchase tests
│ └── test_profile.py # Profile management tests
└── README.md


## Setup Instructions

### Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)

### Installation

1. Clone the repository or create the project structure as shown above
2. Install required Python packages:
   ```bash
   pip install selenium
Running the Application
Start the web server:

bash
python -m http.server 8000
Open your browser and visit:

http://localhost:8000
Running the Tests
Run all tests:

bash
python -m unittest discover tests
Or run individual test files:

bash
python tests/test_registration.py
python tests/test_cart.py
python tests/test_purchase.py
python tests/test_profile.py




BDD Scenarios
User Registration
Successful registration with valid details

Username validation (minimum length)

Email validation (proper format)

Password validation (minimum length and confirmation match)

Shopping Cart
Adding items to cart

Removing items from cart

Applying valid discount code

Applying invalid discount code

Empty cart handling

Product Purchase
Successful purchase with valid payment

Payment failure with missing details

Order summary verification

Payment processing simulation

User Profile Management
Updating profile information successfully

Changing password successfully

Password mismatch handling

Short password validation

Tab switching between profile sections

Test Descriptions
test_registration.py
Tests user registration scenarios including:

Successful registration

Username validation

Email validation

Password validation

test_cart.py
Tests shopping cart functionality including:

Adding/removing items

Discount application

Empty cart handling

test_purchase.py
Tests purchase process including:

Successful checkout

Payment validation

Order summary verification

test_profile.py
Tests profile management including:

Profile information updates

Password changes

Form validations

Development Notes
The application uses localStorage for persistence (cart, profile)

All form validations are done client-side

The payment process simulates success/failure randomly (30% failure rate)

The discount code "DISCOUNT10" applies a 10% discount

Future Enhancements
Server-side persistence

User authentication

Product categories and search

Order history

Responsive design improvements

Troubleshooting
Issue: Tests fail with ChromeDriver errors

Solution: Ensure ChromeDriver version matches your Chrome browser version

Issue: Changes don't persist

Solution: The demo uses localStorage - clear browser cache may reset data

Issue: Payment always fails/succeeds

Solution: The current implementation randomizes results - modify the JavaScript for consistent testing


## Summary of Changes

1. Added Profile link to navigation in all HTML files (as shown in index.html above)
2. Created comprehensive README.md with:
   - Project structure
   - Setup instructions
   - Feature descriptions
   - BDD scenarios
   - Test descriptions
   - Development notes
   - Troubleshooting guide

