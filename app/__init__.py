from flask import Flask
from .extensions import db, login_manager
from app.models.user import User

def create_app():
    app = Flask(__name__)

    import os

    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')


    # Config
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lostfound.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.items import items_bp
    from .routes.admin import admin_bp
    from .routes.profile import profile_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)


    # Create DB tables
    with app.app_context():
        db.create_all()

    # 🔴 THIS LINE MUST EXIST
    return app
