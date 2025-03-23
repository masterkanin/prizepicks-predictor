import os
import sys
import logging
from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append('/home/ubuntu/sports_predictor_web')
from app.api.live_data_pipeline import LiveDataPipeline
from app.models.prediction import db, Prediction, ActualResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/sports_predictor_web/logs/api_routes.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('api_routes')

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize data pipeline
api_key = os.environ.get('SPORTRADAR_API_KEY')
pipeline = LiveDataPipeline(api_key)

@api_bp.route('/update_predictions', methods=['POST'])
def update_predictions():
    """
    Endpoint to trigger prediction updates from Sportradar API
    """
    try:
        # Get days ahead from request or use default
        data = request.get_json() or {}
        days_ahead = data.get('days_ahead', 7)
        
        # Run the pipeline
        num_predictions = pipeline.run_pipeline(days_ahead=days_ahead)
        
        return jsonify({
            'success': True,
            'message': f'Successfully generated {num_predictions} predictions',
            'predictions_count': num_predictions
        }), 200
    except Exception as e:
        logger.error(f"Error updating predictions: {e}")
        return jsonify({
            'success': False,
            'message': f'Error updating predictions: {str(e)}'
        }), 500

@api_bp.route('/upcoming_games', methods=['GET'])
def get_upcoming_games():
    """
    Endpoint to get upcoming games from Sportradar API
    """
    try:
        # Get days ahead from request or use default
        days_ahead = request.args.get('days_ahead', 7, type=int)
        sport = request.args.get('sport')
        
        # Fetch upcoming games
        if sport:
            # Filter by sport if provided
            upcoming_games = {}
            games = pipeline.api.get_upcoming_games(sport, days=days_ahead)
            upcoming_games[sport] = games
        else:
            # Get all sports
            upcoming_games = pipeline.fetch_upcoming_games(days_ahead=days_ahead)
        
        # Format response
        formatted_games = []
        for sport, games in upcoming_games.items():
            for game in games:
                formatted_game = {
                    'id': game.get('id'),
                    'sport': sport,
                    'home_team': game.get('home', {}).get('name'),
                    'away_team': game.get('away', {}).get('name'),
                    'scheduled': game.get('scheduled'),
                    'venue': game.get('venue', {}).get('name') if game.get('venue') else None
                }
                formatted_games.append(formatted_game)
        
        return jsonify({
            'success': True,
            'games_count': len(formatted_games),
            'games': formatted_games
        }), 200
    except Exception as e:
        logger.error(f"Error fetching upcoming games: {e}")
        return jsonify({
            'success': False,
            'message': f'Error fetching upcoming games: {str(e)}'
        }), 500

@api_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """
    Endpoint to get predictions from the database
    """
    try:
        # Get filter parameters
        sport = request.args.get('sport')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        confidence = request.args.get('confidence')
        
        # Build query
        query = Prediction.query
        
        if sport:
            query = query.filter(Prediction.sport == sport)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Prediction.game_date >= date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Prediction.game_date <= date_to_obj)
            except ValueError:
                pass
        
        if confidence:
            query = query.filter(Prediction.confidence == confidence)
        
        # Execute query
        predictions = query.order_by(Prediction.game_date, Prediction.player_name).all()
        
        # Format response
        formatted_predictions = []
        for pred in predictions:
            formatted_pred = {
                'id': pred.id,
                'player_name': pred.player_name,
                'team': pred.team,
                'opponent': pred.opponent,
                'game_date': pred.game_date.strftime('%Y-%m-%d') if pred.game_date else None,
                'sport': pred.sport,
                'stat_type': pred.stat_type,
                'predicted_value': pred.predicted_value,
                'over_probability': pred.over_probability,
                'line': pred.line,
                'confidence': pred.confidence,
                'top_factors': pred.top_factors,
                'created_at': pred.created_at.strftime('%Y-%m-%d %H:%M:%S') if pred.created_at else None
            }
            formatted_predictions.append(formatted_pred)
        
        return jsonify({
            'success': True,
            'predictions_count': len(formatted_predictions),
            'predictions': formatted_predictions
        }), 200
    except Exception as e:
        logger.error(f"Error fetching predictions: {e}")
        return jsonify({
            'success': False,
            'message': f'Error fetching predictions: {str(e)}'
        }), 500

@api_bp.route('/performance', methods=['GET'])
def get_performance():
    """
    Endpoint to get prediction performance metrics
    """
    try:
        # Get filter parameters
        sport = request.args.get('sport')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Build query to join predictions with actual results
        query = db.session.query(
            Prediction, ActualResult
        ).join(
            ActualResult, 
            (Prediction.player_id == ActualResult.player_id) & 
            (Prediction.game_id == ActualResult.game_id) & 
            (Prediction.stat_type == ActualResult.stat_type)
        )
        
        if sport:
            query = query.filter(Prediction.sport == sport)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Prediction.game_date >= date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Prediction.game_date <= date_to_obj)
            except ValueError:
                pass
        
        # Execute query
        results = query.all()
        
        # Calculate performance metrics
        total_predictions = len(results)
        correct_predictions = 0
        high_confidence_total = 0
        high_confidence_correct = 0
        medium_confidence_total = 0
        medium_confidence_correct = 0
        low_confidence_total = 0
        low_confidence_correct = 0
        
        sport_performance = {}
        
        for pred, actual in results:
            # Determine if prediction was correct
            actual_value = actual.actual_value
            line = pred.line
            predicted_over = pred.over_probability > 0.5
            actual_over = actual_value > line
            
            is_correct = (predicted_over == actual_over)
            
            if is_correct:
                correct_predictions += 1
            
            # Track by confidence level
            if pred.confidence == 'High':
                high_confidence_total += 1
                if is_correct:
                    high_confidence_correct += 1
            elif pred.confidence == 'Medium':
                medium_confidence_total += 1
                if is_correct:
                    medium_confidence_correct += 1
            else:  # Low
                low_confidence_total += 1
                if is_correct:
                    low_confidence_correct += 1
            
            # Track by sport
            if pred.sport not in sport_performance:
                sport_performance[pred.sport] = {
                    'total': 0,
                    'correct': 0
                }
            
            sport_performance[pred.sport]['total'] += 1
            if is_correct:
                sport_performance[pred.sport]['correct'] += 1
        
        # Calculate accuracy percentages
        overall_accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
        high_confidence_accuracy = (high_confidence_correct / high_confidence_total) * 100 if high_confidence_total > 0 else 0
        medium_confidence_accuracy = (medium_confidence_correct / medium_confidence_total) * 100 if medium_confidence_total > 0 else 0
        low_confidence_accuracy = (low_confidence_correct / low_confidence_total) * 100 if low_confidence_total > 0 else 0
        
        # Format sport performance
        sport_accuracy = {}
        for sport, data in sport_performance.items():
            sport_accuracy[sport] = {
                'total': data['total'],
                'correct': data['correct'],
                'accuracy': (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
            }
        
        return jsonify({
            'success': True,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'overall_accuracy': round(overall_accuracy, 2),
            'confidence_breakdown': {
                'high': {
                    'total': high_confidence_total,
                    'correct': high_confidence_correct,
                    'accuracy': round(high_confidence_accuracy, 2)
                },
                'medium': {
                    'total': medium_confidence_total,
                    'correct': medium_confidence_correct,
                    'accuracy': round(medium_confidence_accuracy, 2)
                },
                'low': {
                    'total': low_confidence_total,
                    'correct': low_confidence_correct,
                    'accuracy': round(low_confidence_accuracy, 2)
                }
            },
            'sport_breakdown': sport_accuracy
        }), 200
    except Exception as e:
        logger.error(f"Error calculating performance metrics: {e}")
        return jsonify({
            'success': False,
            'message': f'Error calculating performance metrics: {str(e)}'
        }), 500

@api_bp.route('/player/<player_id>', methods=['GET'])
def get_player_details(player_id):
    """
    Endpoint to get player details from Sportradar API
    """
    try:
        # Get sport from request
        sport = request.args.get('sport')
        if not sport:
            return jsonify({
                'success': False,
                'message': 'Sport parameter is required'
            }), 400
        
        # Fetch player profile
        player_profile = pipeline.api.get_player_profile(sport, player_id)
        
        if not player_profile:
            return jsonify({
                'success': False,
                'message': f'Player not found: {player_id}'
            }), 404
        
        # Fetch player stats
        player_stats = pipeline.api.get_player_stats(sport, player_id)
        
        return jsonify({
            'success': True,
            'player_profile': player_profile,
            'player_stats': player_stats
        }), 200
    except Exception as e:
        logger.error(f"Error fetching player details: {e}")
        return jsonify({
            'success': False,
            'message': f'Error fetching player details: {str(e)}'
        }), 500

@api_bp.route('/game/<game_id>', methods=['GET'])
def get_game_details(game_id):
    """
    Endpoint to get game details from Sportradar API
    """
    try:
        # Get sport from request
        sport = request.args.get('sport')
        if not sport:
            return jsonify({
                'success': False,
                'message': 'Sport parameter is required'
            }), 400
        
        # Fetch game summary
        game_summary = pipeline.api.get_game_summary(sport, game_id)
        
        if not game_summary:
            return jsonify({
                'success': False,
                'message': f'Game not found: {game_id}'
            }), 404
        
        return jsonify({
            'success': True,
            'game_summary': game_summary
        }), 200
    except Exception as e:
        logger.error(f"Error fetching game details: {e}")
        return jsonify({
            'success': False,
            'message': f'Error fetching game details: {str(e)}'
        }), 500
