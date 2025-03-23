"""
Deployment script for PrizePicks Predictor web application.
This script handles the deployment of the web application to a production environment.
"""

import os
import sys
import logging
import argparse
import subprocess
import shutil
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/deployment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('deployment')

# Paths
WEB_APP_PATH = '.'
VENV_PATH = os.path.join(WEB_APP_PATH, 'venv')
VENV_PYTHON = os.path.join(VENV_PATH, 'bin', 'python')
VENV_PIP = os.path.join(VENV_PATH, 'bin', 'pip')

def check_dependencies():
    """
    Check if all required dependencies are installed.
    
    Returns:
        True if all dependencies are installed, False otherwise
    """
    logger.info("Checking dependencies")
    
    try:
        # Check Python version
        python_version = subprocess.run([VENV_PYTHON, '--version'], capture_output=True, text=True, check=True)
        logger.info(f"Python version: {python_version.stdout.strip()}")
        
        # Check pip packages
        required_packages = [
            'flask', 'flask-sqlalchemy', 'gunicorn', 'pandas', 'numpy', 
            'matplotlib', 'plotly', 'requests'
        ]
        
        for package in required_packages:
            result = subprocess.run(
                [VENV_PIP, 'show', package], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Package {package} is not installed")
                return False
            
            logger.info(f"Package {package} is installed")
        
        return True
    except Exception as e:
        logger.error(f"Error checking dependencies: {e}")
        return False

def setup_production_config():
    """
    Set up production configuration for the web application.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Setting up production configuration")
    
    try:
        # Create production config file
        config_path = os.path.join(WEB_APP_PATH, 'config.py')
        with open(config_path, 'w') as f:
            f.write("""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///predictions.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
""")
        
        # Update app/__init__.py to use config
        init_path = os.path.join(WEB_APP_PATH, 'app', '__init__.py')
        with open(init_path, 'r') as f:
            content = f.read()
        
        if 'config' not in content:
            # Add config import
            new_content = """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import config

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.predictions import predictions_bp
    app.register_blueprint(predictions_bp, url_prefix='/predictions')
    
    return app
"""
            with open(init_path, 'w') as f:
                f.write(new_content)
        
        # Create wsgi.py file
        wsgi_path = os.path.join(WEB_APP_PATH, 'wsgi.py')
        with open(wsgi_path, 'w') as f:
            f.write("""from app import create_app

app = create_app('production')

if __name__ == '__main__':
    app.run()
""")
        
        # Create gunicorn config
        gunicorn_path = os.path.join(WEB_APP_PATH, 'gunicorn_config.py')
        with open(gunicorn_path, 'w') as f:
            f.write("""import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
accesslog = "logs/access.log"
errorlog = "logs/error.log"
""")
        
        return True
    except Exception as e:
        logger.error(f"Error setting up production configuration: {e}")
        return False

def create_systemd_service():
    """
    Create a systemd service for the web application.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Creating systemd service")
    
    try:
        # Create service file
        service_content = f"""[Unit]
Description=PrizePicks Predictor Web Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory={WEB_APP_PATH}
Environment="PATH={VENV_PATH}/bin"
Environment="FLASK_ENV=production"
ExecStart={VENV_PATH}/bin/gunicorn --config {WEB_APP_PATH}/gunicorn_config.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
"""
        
        service_path = '/tmp/prizepicks-predictor.service'
        with open(service_path, 'w') as f:
            f.write(service_content)
        
        # Copy to systemd directory (requires sudo)
        try:
            subprocess.run(['sudo', 'cp', service_path, '/etc/systemd/system/'], check=True)
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            logger.info("Systemd service created successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing systemd service: {e}")
            logger.info("Service file created at: {service_path}")
            logger.info("To install manually, run: sudo cp {service_path} /etc/systemd/system/ && sudo systemctl daemon-reload")
            return False
    except Exception as e:
        logger.error(f"Error creating systemd service: {e}")
        return False

def create_nginx_config():
    """
    Create an Nginx configuration for the web application.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Creating Nginx configuration")
    
    try:
        # Create nginx config file
        nginx_content = """server {
    listen 80;
    server_name _;  # Replace with your domain name if available

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ubuntu/sports_predictor_web/app/static;
        expires 30d;
    }
}
"""
        
        nginx_path = '/tmp/prizepicks-predictor.nginx'
        with open(nginx_path, 'w') as f:
            f.write(nginx_content)
        
        # Copy to nginx directory (requires sudo)
        try:
            subprocess.run(['sudo', 'cp', nginx_path, '/etc/nginx/sites-available/prizepicks-predictor'], check=True)
            subprocess.run(['sudo', 'ln', '-sf', '/etc/nginx/sites-available/prizepicks-predictor', '/etc/nginx/sites-enabled/'], check=True)
            subprocess.run(['sudo', 'nginx', '-t'], check=True)  # Test nginx config
            subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
            logger.info("Nginx configuration created successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing nginx configuration: {e}")
            logger.info(f"Nginx config file created at: {nginx_path}")
            logger.info(f"To install manually, run: sudo cp {nginx_path} /etc/nginx/sites-available/prizepicks-predictor && sudo ln -sf /etc/nginx/sites-available/prizepicks-predictor /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx")
            return False
    except Exception as e:
        logger.error(f"Error creating nginx configuration: {e}")
        return False

def start_services():
    """
    Start the web application services.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting services")
    
    try:
        # Enable and start systemd service
        subprocess.run(['sudo', 'systemctl', 'enable', 'prizepicks-predictor'], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'prizepicks-predictor'], check=True)
        logger.info("Services started successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting services: {e}")
        return False

def deploy():
    """
    Deploy the web application.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting deployment")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed")
        return False
    
    # Set up production configuration
    if not setup_production_config():
        logger.error("Production configuration setup failed")
        return False
    
    # Create systemd service
    if not create_systemd_service():
        logger.warning("Systemd service creation failed, continuing with deployment")
    
    # Create nginx config
    if not create_nginx_config():
        logger.warning("Nginx configuration creation failed, continuing with deployment")
    
    # Start services
    if not start_services():
        logger.warning("Service startup failed, continuing with deployment")
    
    logger.info("Deployment completed")
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Deployment Script for PrizePicks Predictor')
    
    parser.add_argument('--check-only', action='store_true',
                        help='Only check dependencies without deploying')
    
    args = parser.parse_args()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.join(WEB_APP_PATH, 'logs'), exist_ok=True)
    
    if args.check_only:
        success = check_dependencies()
    else:
        success = deploy()
    
    if success:
        logger.info("Operation completed successfully")
        return 0
    else:
        logger.error("Operation failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
