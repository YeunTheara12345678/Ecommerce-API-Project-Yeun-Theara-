import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# INIT EXTENSIONS
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

# Token blacklist (for logout)
jwt_blacklist = set()


def create_app():
    app = Flask(__name__)

    # CONFIG
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///ecommerce.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY', 'secret-key'
    )

    # INIT EXTENSIONS
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # REGISTER BLUEPRINTS
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.customer import customer_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(customer_bp, url_prefix='/api/front')
    return app


# JWT LOGOUT CHECK
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blacklist


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
