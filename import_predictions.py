"""
Import sample prediction data into the database.
This script reads the JSON files and populates the database with prediction records.
"""

import os
import json
from datetime import datetime
from app import create_app, db
from app.models.prediction import Prediction, ActualResult

def import_predictions():
    """Import predictions from JSON files into the database"""
    # Initialize Flask app context
    app = create_app()
    with app.app_context():
        # Get predictions directory
        predictions_dir = '/home/ubuntu/sports_predictor/home/ubuntu/neural_sports_predictor/output/predictions'
        
        if not os.path.exists(predictions_dir):
            print(f"Error: Predictions directory not found: {predictions_dir}")
            return
        
        # Find JSON files
        json_files = [f for f in os.listdir(predictions_dir) if f.endswith('.json')]
        if not json_files:
            print("No JSON files found in directory")
            return
        
        # Process each file
        imported_count = 0
        for filename in json_files:
            file_path = os.path.join(predictions_dir, filename)
            
            # Extract sport from filename (format: predictions_YYYY-MM-DD_sport.json)
            parts = filename.split('_')
            if len(parts) >= 3:
                sport = parts[2].split('.')[0]  # Remove .json extension
            else:
                sport = 'unknown'
            
            # Extract date from filename
            try:
                date_str = parts[1]
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except (ValueError, IndexError):
                date = datetime.now().date()
            
            print(f"Processing {filename} for {sport} on {date}")
            
            # Load JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Process predictions
            file_count = 0
            for pred_data in data:
                # Create new prediction
                new_prediction = Prediction(
                    player=pred_data.get('player', ''),
                    team=pred_data.get('team', ''),
                    opponent=pred_data.get('opponent', ''),
                    sport=sport,
                    date=date,
                    stat=pred_data.get('stat', ''),
                    predicted_value=pred_data.get('predicted_value', 0.0),
                    over_probability=pred_data.get('over_probability', 0.5),
                    line=pred_data.get('line'),
                    confidence=pred_data.get('confidence', 'Medium'),
                    confidence_score=pred_data.get('confidence_score', 50.0)
                )
                
                # Handle prediction range
                pred_range = pred_data.get('prediction_range')
                if pred_range and len(pred_range) == 2:
                    new_prediction.prediction_range_low = pred_range[0]
                    new_prediction.prediction_range_high = pred_range[1]
                
                # Handle top factors
                top_factors = pred_data.get('top_factors')
                if top_factors:
                    new_prediction.top_factors = '|'.join(top_factors)
                
                db.session.add(new_prediction)
                file_count += 1
                imported_count += 1
            
            print(f"Imported {file_count} predictions from {filename}")
            db.session.commit()
        
        # Add some actual results for past predictions (for demonstration purposes)
        print("Adding sample actual results for past predictions...")
        
        # Get predictions from past days (not today)
        today = datetime.now().date()
        past_predictions = Prediction.query.filter(Prediction.date < today).limit(100).all()
        
        results_count = 0
        for prediction in past_predictions:
            # Generate a realistic actual result
            if prediction.line:
                # 60% chance of being correct (for demonstration)
                correct = (results_count % 10) < 6
                
                if prediction.over_probability > 0.5:
                    # Model predicted over
                    if correct:
                        actual_value = prediction.line + (prediction.predicted_value - prediction.line) * 1.1
                        result = 'over'
                    else:
                        actual_value = prediction.line - (prediction.line - prediction.predicted_value) * 0.5
                        result = 'under'
                else:
                    # Model predicted under
                    if correct:
                        actual_value = prediction.line - (prediction.line - prediction.predicted_value) * 1.1
                        result = 'under'
                    else:
                        actual_value = prediction.line + (prediction.predicted_value - prediction.line) * 0.5
                        result = 'over'
                
                # Create actual result
                actual_result = ActualResult(
                    prediction_id=prediction.id,
                    actual_value=round(actual_value, 1),
                    result=result
                )
                
                db.session.add(actual_result)
                results_count += 1
        
        db.session.commit()
        print(f"Added {results_count} actual results for past predictions")
        
        print(f"Successfully imported {imported_count} predictions into the database.")

if __name__ == '__main__':
    import_predictions()
