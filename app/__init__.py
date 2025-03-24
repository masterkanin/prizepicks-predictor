from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
import logging
from app.models.prediction import db
from app.routes.main import main_bp
from app.routes.predictions import predictions_bp
from app.routes.api import api_bp
from app.routes.import_route import import_bp
app.register_blueprint(import_bp, url_prefix='/import')


def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SPORTRADAR_API_KEY=os.environ.get('SPORTRADAR_API_KEY', '')
    )
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join('logs', 'app.log')),
            logging.StreamHandler()
        ]
    )
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(predictions_bp, url_prefix='/predictions')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
