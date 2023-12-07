from flask import session

# Function to calculate the cart item count
def calculate_cart_item_count():
    # Checking if 'cart' is in the session
    if 'cart' in session:
        # Summing the quantities of all items in the cart
        item_count = sum(item['quantity'] for item in session['cart'].values())
        return item_count
    else:
        # Returning 0 if 'cart' is not in the session
        return 0