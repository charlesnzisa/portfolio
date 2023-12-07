from flask import Flask
from app.extensions import migrate
from flask_login import LoginManager

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initializing Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    #specifying the user loader
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Registerng blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.categories import bp as categories_bp
    app.register_blueprint(categories_bp)

    from app.products import bp as products_bp
    app.register_blueprint(products_bp)

    from app.cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from app.calculate_cart_total import bp as total_bp
    app.register_blueprint(total_bp)

    from app.cart_item_count import bp as count_bp
    app.register_blueprint(count_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app