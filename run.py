from app import create_app, db
from app.models.prediction import Prediction, ActualResult

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print('Database initialized.')

@app.cli.command('import-predictions')
def import_predictions():
    """Import predictions from the neural sports predictor output."""
    import os
    import json
    from datetime import datetime
    
    predictor_output_dir = '/home/ubuntu/sports_predictor/home/ubuntu/neural_sports_predictor/output/predictions'
    
    if not os.path.exists(predictor_output_dir):
        print(f"Predictor output directory not found: {predictor_output_dir}")
        return
    
    with app.app_context():
        # Find JSON files
        json_files = [f for f in os.listdir(predictor_output_dir) if f.endswith('.json')]
        if not json_files:
            print('No JSON files found in directory')
            return
        
        # Process each file
        imported_count = 0
        for filename in json_files:
            file_path = os.path.join(predictor_output_dir, filename)
            
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
            
            # Load JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Process predictions
            for pred_data in data:
                # Check if prediction already exists
                existing = Prediction.query.filter_by(
                    player=pred_data.get('player'),
                    date=date,
                    stat=pred_data.get('stat')
                ).first()
                
                if existing:
                    # Update existing prediction
                    existing.team = pred_data.get('team', '')
                    existing.opponent = pred_data.get('opponent', '')
                    existing.predicted_value = pred_data.get('predicted_value', 0.0)
                    existing.over_probability = pred_data.get('over_probability', 0.5)
                    existing.line = pred_data.get('line')
                    existing.confidence = pred_data.get('confidence', 'Medium')
                    existing.confidence_score = pred_data.get('confidence_score', 50.0)
                    
                    # Handle prediction range
                    pred_range = pred_data.get('prediction_range')
                    if pred_range and len(pred_range) == 2:
                        existing.prediction_range_low = pred_range[0]
                        existing.prediction_range_high = pred_range[1]
                    
                    # Handle top factors
                    top_factors = pred_data.get('top_factors')
                    if top_factors:
                        existing.top_factors = '|'.join(top_factors)
                else:
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
                    imported_count += 1
            
            db.session.commit()
        
        print(f'Successfully imported {imported_count} predictions')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
