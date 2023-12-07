from flask import session

def calculate_cart_total():
    total = 0

    if 'cart' in session:
        for product_id, product_info in session['cart'].items():
            price = float(product_info['price'])
            quantity = int(product_info['quantity'])
            total += price * quantity

    return total