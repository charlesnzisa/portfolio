from . import bp
from flask import render_template
from flask_login import login_required
from app.models.product import Product

@bp.route('/product')
@login_required
def product():
    products=Product.query.all()
    return render_template('products/product.html', products=products)