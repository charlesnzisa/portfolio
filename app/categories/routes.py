from . import bp
from flask import render_template
from app.models.category import Category

@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html')