from flask import render_template, session, flash, redirect, url_for, request, jsonify
from app.models.product import Product
from . import bp
from app.calculate_cart_total.total import calculate_cart_total
from app.cart_item_count.item_count import calculate_cart_item_count
from flask import current_app


#[------------------------add_to_cart_logic----------------------------]
@bp.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        # Initializing cart in the session if not present
        if 'cart' not in session:
            session['cart'] = {}

        if request.method == 'POST':
            # Converting product_id to string for session key
            product_id_str = str(product_id)

            # Converting quantity to int
            quantity = int(request.form.get('quantity', 1))

            # Retrieving the current quantity from the session
            current_quantity = int(session['cart'].get(product_id_str, {}).get('quantity', 0))

            # Updating the session data with the new quantity
            session['cart'][product_id_str] = {
                'name': product.name,
                'price': product.price,
                'quantity': current_quantity + quantity
            }

            flash('Item added to cart', 'success')
            session.modified = True

        return redirect(url_for('cart.cart_content'))

    except Exception as e:
        current_app.logger.error(f"Error in add_to_cart: {e}")
        current_app.logger.error(f"Session data: {session}")
        flash('Error adding item to cart', 'error')
        return redirect(url_for('cart.cart_content'))



#[--------------------cart_content--------------------]
@bp.route('/cart_content')
def cart_content():
    cart_total = calculate_cart_total()
    cart_data=session.get('cart', {})
    return render_template('cart/cart.html', cart=cart_data, cart_total=cart_total)

# ---------------------route for fetching cart item count--------------------
# New route for fetching cart item count
@bp.route('/get_cart_item_count')
def get_cart_item_count():
    item_count = calculate_cart_item_count()
    return jsonify({'itemCount': item_count})

#[---------------------Add_more_logic---------------------]
@bp.route('/add_more/<int:product_id>', methods=['POST'])
def add_more(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            # Converting product_id to string for session key
            product_id_str = str(product_id)

            # Converting quantity to int
            quantity = int(request.form.get('quantity', 1))

            # Calling the add_more_logic function
            add_more_logic(product, quantity)

        return redirect(url_for('cart.cart_content'))

    except Exception as e:
        current_app.logger.error(f"Error in add_more route: {e}")
        current_app.logger.error(f"Session data: {session}")
        flash('Error updating item quantity in cart', 'error')
        return redirect(url_for('cart.cart_content'))

def add_more_logic(product, quantity):
    if product:
        if 'cart' not in session:
            session['cart'] = {}

        if product.id in session['cart']:
            current_quantity = int(session['cart'][product.id]['quantity'])
            session['cart'][product.id]['quantity'] = current_quantity + quantity
            flash('Item quantity updated in cart', 'success')
            session.modified = True
        else:
            flash('Product not found in the cart', 'error')
    else:
        flash('Product not found', 'error')

    return redirect(url_for('cart.cart_content'))


#[--------------------------DELETE_ITEM---------------------------]
@bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session and str(product_id) in session['cart']:
        del session['cart'][str(product_id)]
        flash('Item removed from cart', 'success')
        session.modified = True
    else:
        flash('Item not found in cart', 'error')

    return redirect(url_for('cart.cart_content'))
