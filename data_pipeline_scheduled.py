"""
Scheduled data pipeline for PrizePicks sports prediction system.
This script fetches live data from Sportradar API every 10 minutes and updates predictions.
"""

import os
import sys
import json
import time
import logging
import argparse
import schedule
from datetime import datetime, timedelta
import requests
from app import create_app, db
from app.models.prediction import Prediction
from app.api.sportradar_client import SportradarAPI
from app.api.live_data_pipeline import LiveDataPipeline

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_pipeline')

def run_pipeline():
    """
    Run the data pipeline to fetch live data and update predictions.
    """
    logger.info("Starting data pipeline run")
    
    try:
        # Create Flask app context
        app = create_app()
        with app.app_context():
            # Initialize the live data pipeline
            pipeline = LiveDataPipeline()
            
            # Fetch data for all major sports
            sports = ['nba', 'nfl', 'mlb', 'nhl', 'soccer']
            
            for sport in sports:
                logger.info(f"Processing {sport.upper()} data")
                try:
                    # Fetch live data
                    data = pipeline.fetch_data(sport)
                    
                    # Generate predictions
                    predictions = pipeline.generate_predictions(data, sport)
                    
                    # Save predictions to database
                    count = pipeline.save_predictions(predictions)
                    
                    logger.info(f"Successfully processed {count} predictions for {sport.upper()}")
                except Exception as e:
                    logger.error(f"Error processing {sport} data: {str(e)}")
            
            # Clean up old predictions (older than 30 days)
            thirty_days_ago = datetime.now().date() - timedelta(days=30)
            old_predictions = Prediction.query.filter(Prediction.date < thirty_days_ago).all()
            for pred in old_predictions:
                db.session.delete(pred)
            db.session.commit()
            logger.info(f"Cleaned up {len(old_predictions)} old predictions")
            
            logger.info("Data pipeline run completed successfully")
    except Exception as e:
        logger.error(f"Error in data pipeline: {str(e)}")

def schedule_pipeline():
    """
    Schedule the data pipeline to run every 10 minutes.
    """
    logger.info("Starting scheduled data pipeline")
    
    # Run immediately on startup
    run_pipeline()
    
    # Schedule to run every 10 minutes
    schedule.every(10).minutes.do(run_pipeline)
    
    logger.info("Pipeline scheduled to run every 10 minutes")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='PrizePicks Data Pipeline')
    
    parser.add_argument('--schedule', action='store_true',
                        help='Run the pipeline on a schedule (every 10 minutes)')
    
    args = parser.parse_args()
    
    if args.schedule:
        schedule_pipeline()
    else:
        run_pipeline()

if __name__ == '__main__':
    main()
