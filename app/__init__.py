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

    from app.models.user import User
    from werkzeug.security import generate_password_hash

    from app.models.user import User
    from werkzeug.security import generate_password_hash

    with app.app_context():
        db.create_all()

        # FORCE admin creation if missing
        admin = User.query.filter_by(email="admin@lostfound.com").first()
        if not admin:
            admin = User(
                username="admin",
                full_name="Admin",
                email="admin@lostfound.com",
                contact_number="9999999999",
                password=generate_password_hash("admin123"),
                role="admin",
                is_blocked=False
            )
            db.session.add(admin)
            db.session.commit()


    return app
