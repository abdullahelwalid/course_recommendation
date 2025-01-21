from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config  # Import your configuration class
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(Config)  # Load configuration from Config class
        db.init_app(app)  # Initialize database
        db.create_all()  # Create tables if they don't exist
        Migrate(app, db)
        bcrypt.init_app(app)  # Initialize Bcrypt

        # Import and register blueprints
        from routes.routes import bp
        from routes.admin import admin
        app.register_blueprint(bp)
        app.register_blueprint(admin)

        return app, db, bcrypt

app, db, bcrypt = create_app()

if __name__ == "__main__":
    app.run(debug=True)
