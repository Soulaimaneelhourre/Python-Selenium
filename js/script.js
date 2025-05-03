// Cart functionality
let cart = [];
let discountApplied = false;

// Load cart from localStorage
function loadCart() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartCount();
    }
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

// Update cart count in navigation
function updateCartCount() {
    const countElements = document.querySelectorAll('#cart-count');
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    countElements.forEach(el => el.textContent = totalItems);
}

// Add item to cart
function addToCart(name, price) {
    const existingItem = cart.find(item => item.name === name);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name, price, quantity: 1 });
    }
    
    saveCart();
    alert(`${name} added to cart!`);
}

// Remove item from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    displayCartItems();
}

// Display cart items
function displayCartItems() {
    const cartItemsElement = document.getElementById('cart-items');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    
    if (cart.length === 0) {
        cartItemsElement.innerHTML = '<p>Your cart is empty.</p>';
        subtotalElement.textContent = '0.00';
        totalElement.textContent = '0.00';
        return;
    }
    
    let html = '';
    let subtotal = 0;
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        html += `
            <div class="cart-item">
                <div>
                    <h3>${item.name}</h3>
                    <p>$${item.price.toFixed(2)} x ${item.quantity}</p>
                </div>
                <div>
                    <p>$${itemTotal.toFixed(2)}</p>
                    <button onclick="removeFromCart(${index})">Remove</button>
                </div>
            </div>
        `;
    });
    
    cartItemsElement.innerHTML = html;
    subtotalElement.textContent = subtotal.toFixed(2);
    
    // Apply discount if any
    const total = discountApplied ? subtotal * 0.9 : subtotal;
    totalElement.textContent = total.toFixed(2);
}

// Apply discount
function applyDiscount() {
    const discountCode = document.getElementById('discount-code').value;
    const discountMessage = document.getElementById('discount-message');
    
    if (discountCode === 'DISCOUNT10') {
        discountApplied = true;
        discountMessage.textContent = '10% discount applied!';
        discountMessage.style.color = 'green';
        displayCartItems();
    } else {
        discountApplied = false;
        discountMessage.textContent = 'Invalid discount code';
        discountMessage.style.color = 'red';
        displayCartItems();
    }
}

// Proceed to checkout
function proceedToCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    window.location.href = 'checkout.html';
}

// Display checkout summary
function displayCheckoutSummary() {
    const checkoutSummary = document.getElementById('checkout-summary');
    let html = '<h3>Order Summary</h3>';
    let subtotal = 0;
    
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        html += `
            <div class="checkout-item">
                <p>${item.name} - $${item.price.toFixed(2)} x ${item.quantity} = $${itemTotal.toFixed(2)}</p>
            </div>
        `;
    });
    
    const total = discountApplied ? subtotal * 0.9 : subtotal;
    
    html += `
        <div class="checkout-totals">
            <p><strong>Subtotal:</strong> $${subtotal.toFixed(2)}</p>
            ${discountApplied ? `<p><strong>Discount (10%):</strong> -$${(subtotal * 0.1).toFixed(2)}</p>` : ''}
            <p><strong>Total:</strong> $${total.toFixed(2)}</p>
        </div>
    `;
    
    checkoutSummary.innerHTML = html;
}

// Handle payment form submission
function handlePaymentForm(event) {
    event.preventDefault();
    const paymentResult = document.getElementById('payment-result');
    
    // Simple validation
    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;
    
    if (!cardNumber || !expiryDate || !cvv) {
        paymentResult.innerHTML = '<p class="error-message">Please fill in all payment details.</p>';
        return;
    }
    
    // Simulate payment processing
    setTimeout(() => {
        // Randomly succeed or fail for testing
        const success = Math.random() > 0.3;
        
        if (success) {
            paymentResult.innerHTML = `
                <div class="success-message">
                    <p>Payment successful! Thank you for your purchase.</p>
                    <p>Order confirmation will be sent to your email.</p>
                </div>
            `;
            // Clear cart
            cart = [];
            saveCart();
        } else {
            paymentResult.innerHTML = '<p class="error-message">Payment failed. Please try again or use a different payment method.</p>';
        }
    }, 1500);
}

// Registration form validation
function validateRegistrationForm(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    let isValid = true;
    
    // Validate username
    if (username.length < 4) {
        document.getElementById('username-error').textContent = 'Username must be at least 4 characters';
        isValid = false;
    } else {
        document.getElementById('username-error').textContent = '';
    }
    
    // Validate email
    if (!email.includes('@') || !email.includes('.')) {
        document.getElementById('email-error').textContent = 'Please enter a valid email address';
        isValid = false;
    } else {
        document.getElementById('email-error').textContent = '';
    }
    
    // Validate password
    if (password.length < 6) {
        document.getElementById('password-error').textContent = 'Password must be at least 6 characters';
        isValid = false;
    } else {
        document.getElementById('password-error').textContent = '';
    }
    
    // Validate password confirmation
    if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = 'Passwords do not match';
        isValid = false;
    } else {
        document.getElementById('confirm-password-error').textContent = '';
    }
    
    // If all valid, show success message
    if (isValid) {
        document.getElementById('registration-success').textContent = 'Registration successful! Redirecting...';
        setTimeout(() => {
            window.location.href = 'products.html';
        }, 2000);
    }
}

function openTab(tabId) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }
    
    // Remove active class from all buttons
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    // Show the selected tab and mark button as active
    document.getElementById(tabId).style.display = 'block';
    event.currentTarget.classList.add('active');
}

function loadProfile() {
    // In a real app, this would load from server
    // For demo, we'll use localStorage or default values
    const profile = JSON.parse(localStorage.getItem('userProfile')) || {
        fullName: '',
        email: localStorage.getItem('registeredEmail') || '',
        address: '',
        phone: ''
    };
    
    document.getElementById('full-name').value = profile.fullName;
    document.getElementById('profile-email').value = profile.email;
    document.getElementById('address').value = profile.address;
    document.getElementById('phone').value = profile.phone;
}

function saveProfile() {
    const profile = {
        fullName: document.getElementById('full-name').value,
        email: document.getElementById('profile-email').value,
        address: document.getElementById('address').value,
        phone: document.getElementById('phone').value
    };
    
    localStorage.setItem('userProfile', JSON.stringify(profile));
}

function handleProfileForm(event) {
    event.preventDefault();
    saveProfile();
    
    const resultDiv = document.getElementById('profile-update-result');
    resultDiv.innerHTML = '<p class="success-message">Profile updated successfully!</p>';
    
    setTimeout(() => {
        resultDiv.innerHTML = '';
    }, 3000);
}

function validatePasswordForm(event) {
    event.preventDefault();
    
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmNewPassword = document.getElementById('confirm-new-password').value;
    
    let isValid = true;
    
    // Validate current password (in real app, would check against stored password)
    if (!currentPassword) {
        document.getElementById('current-password-error').textContent = 'Please enter your current password';
        isValid = false;
    } else {
        document.getElementById('current-password-error').textContent = '';
    }
    
    // Validate new password
    if (newPassword.length < 6) {
        document.getElementById('new-password-error').textContent = 'Password must be at least 6 characters';
        isValid = false;
    } else {
        document.getElementById('new-password-error').textContent = '';
    }
    
    // Validate password confirmation
    if (newPassword !== confirmNewPassword) {
        document.getElementById('confirm-new-password-error').textContent = 'Passwords do not match';
        isValid = false;
    } else {
        document.getElementById('confirm-new-password-error').textContent = '';
    }
    
    // If all valid, show success message
    if (isValid) {
        const resultDiv = document.getElementById('password-change-result');
        resultDiv.innerHTML = '<p class="success-message">Password changed successfully!</p>';
        
        // Clear form
        document.getElementById('passwordForm').reset();
        
        setTimeout(() => {
            resultDiv.innerHTML = '';
        }, 3000);
    }
}

// Update initPage function to include profile management
function initPage() {
    loadCart();
    
    // Initialize registration form if it exists
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', validateRegistrationForm);
    }
    
    // Initialize cart display if on cart page
    if (document.getElementById('cart-items')) {
        displayCartItems();
    }
    
    // Initialize checkout summary if on checkout page
    if (document.getElementById('checkout-summary')) {
        displayCheckoutSummary();
    }
    
    // Initialize payment form if it exists
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', handlePaymentForm);
    }
    
    // Initialize profile management if on profile page
    if (document.getElementById('profileForm')) {
        loadProfile();
        document.getElementById('profileForm').addEventListener('submit', handleProfileForm);
        document.getElementById('passwordForm').addEventListener('submit', validatePasswordForm);
    }
}

// Initialize page
function initPage() {
    loadCart();
    
    // Initialize registration form if it exists
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', validateRegistrationForm);
    }
    
    // Initialize cart display if on cart page
    if (document.getElementById('cart-items')) {
        displayCartItems();
    }
    
    // Initialize checkout summary if on checkout page
    if (document.getElementById('checkout-summary')) {
        displayCheckoutSummary();
    }
    
    // Initialize payment form if it exists
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', handlePaymentForm);
    }
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initPage);