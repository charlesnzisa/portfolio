from flask import render_template
from flask_login import login_required, current_user
from . import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)