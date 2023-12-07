from flask import Blueprint

bp=Blueprint('calculate_cart_total', __name__)

from . import total