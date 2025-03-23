"""
Data pipeline integration script for PrizePicks Predictor web application.
This script connects the neural network sports prediction system with the web application.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
import subprocess
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_pipeline')

# Paths
PREDICTOR_PATH = '/home/ubuntu/sports_predictor/home/ubuntu/neural_sports_predictor'
WEB_APP_PATH = '.'
PREDICTIONS_OUTPUT_DIR = os.path.join(PREDICTOR_PATH, 'output', 'predictions')
WEB_APP_VENV = os.path.join(WEB_APP_PATH, 'venv', 'bin', 'python')

def run_predictor(mode='predict', sport=None, date=None):
    """
    Run the neural network sports predictor with specified parameters.
    
    Args:
        mode: Operation mode (collect, train, predict, full)
        sport: Sport to process (default: all)
        date: Date to process in YYYY-MM-DD format (default: today)
    
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Running predictor in {mode} mode")
    
    # Build command
    cmd = [sys.executable, os.path.join(PREDICTOR_PATH, 'main.py'), f'--mode={mode}']
    
    if sport:
        cmd.append(f'--sport={sport}')
    
    if date:
        cmd.append(f'--date={date}')
    
    # Run command
    try:
        logger.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=PREDICTOR_PATH, check=True, capture_output=True, text=True)
        logger.info(f"Predictor output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running predictor: {e}")
        logger.error(f"Stderr: {e.stderr}")
        return False

def import_predictions_to_webapp():
    """
    Import predictions from the neural network output to the web application database.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Importing predictions to web application")
    
    # Check if predictions directory exists
    if not os.path.exists(PREDICTIONS_OUTPUT_DIR):
        logger.error(f"Predictions directory not found: {PREDICTIONS_OUTPUT_DIR}")
        return False
    
    # Check if there are any prediction files
    prediction_files = [f for f in os.listdir(PREDICTIONS_OUTPUT_DIR) if f.endswith('.json')]
    if not prediction_files:
        logger.error("No prediction files found")
        return False
    
    # Run import script
    try:
        cmd = [WEB_APP_VENV, os.path.join(WEB_APP_PATH, 'import_predictions.py')]
        logger.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=WEB_APP_PATH, check=True, capture_output=True, text=True)
        logger.info(f"Import output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error importing predictions: {e}")
        logger.error(f"Stderr: {e.stderr}")
        return False

def run_full_pipeline(date=None):
    """
    Run the full pipeline: data collection, training, prediction, and import to web app.
    
    Args:
        date: Date to process in YYYY-MM-DD format (default: today)
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Running full pipeline")
    
    # Run data collection
    if not run_predictor(mode='collect', date=date):
        logger.error("Data collection failed")
        return False
    
    # Run training
    if not run_predictor(mode='train', date=date):
        logger.error("Training failed")
        return False
    
    # Run prediction
    if not run_predictor(mode='predict', date=date):
        logger.error("Prediction failed")
        return False
    
    # Import predictions to web app
    if not import_predictions_to_webapp():
        logger.error("Prediction import failed")
        return False
    
    logger.info("Full pipeline completed successfully")
    return True

def setup_cron_job():
    """
    Set up a cron job to run the pipeline daily.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Setting up cron job")
    
    # Create cron job script
    cron_script_path = os.path.join(WEB_APP_PATH, 'run_pipeline.sh')
    with open(cron_script_path, 'w') as f:
        f.write(f"""#!/bin/bash
cd {WEB_APP_PATH}
{sys.executable} {os.path.join(WEB_APP_PATH, 'data_pipeline.py')} --mode=full
""")
    
    # Make script executable
    os.chmod(cron_script_path, 0o755)
    
    # Add to crontab (runs at 2 AM daily)
    cron_cmd = f"0 2 * * * {cron_script_path} >> {os.path.join(WEB_APP_PATH, 'logs', 'cron.log')} 2>&1"
    
    try:
        # Write to temporary file
        temp_cron_file = '/tmp/crontab.txt'
        subprocess.run(['crontab', '-l'], stdout=open(temp_cron_file, 'w'), stderr=subprocess.DEVNULL)
        
        # Check if entry already exists
        with open(temp_cron_file, 'r') as f:
            cron_content = f.read()
        
        if cron_script_path not in cron_content:
            # Append new cron job
            with open(temp_cron_file, 'a') as f:
                f.write(f"{cron_cmd}\n")
            
            # Install new crontab
            subprocess.run(['crontab', temp_cron_file], check=True)
            logger.info("Cron job installed successfully")
        else:
            logger.info("Cron job already exists")
        
        # Clean up
        os.remove(temp_cron_file)
        return True
    except Exception as e:
        logger.error(f"Error setting up cron job: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Data Pipeline Integration for PrizePicks Predictor')
    
    parser.add_argument('--mode', type=str, default='import',
                        choices=['collect', 'train', 'predict', 'import', 'full', 'setup-cron'],
                        help='Operation mode')
    
    parser.add_argument('--sport', type=str, default=None,
                        help='Sport to process (default: all)')
    
    parser.add_argument('--date', type=str, default=None,
                        help='Date to process in YYYY-MM-DD format (default: today)')
    
    args = parser.parse_args()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.join(WEB_APP_PATH, 'logs'), exist_ok=True)
    
    # Process based on mode
    if args.mode == 'collect':
        success = run_predictor(mode='collect', sport=args.sport, date=args.date)
    elif args.mode == 'train':
        success = run_predictor(mode='train', sport=args.sport, date=args.date)
    elif args.mode == 'predict':
        success = run_predictor(mode='predict', sport=args.sport, date=args.date)
    elif args.mode == 'import':
        success = import_predictions_to_webapp()
    elif args.mode == 'full':
        success = run_full_pipeline(date=args.date)
    elif args.mode == 'setup-cron':
        success = setup_cron_job()
    else:
        logger.error(f"Invalid mode: {args.mode}")
        return 1
    
    if success:
        logger.info(f"{args.mode} completed successfully")
        return 0
    else:
        logger.error(f"{args.mode} failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
