from flask import Blueprint, render_template, request, jsonify
import logging
from datetime import datetime, timedelta
from app.models.prediction import db, Prediction, Game, Player, Team

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/sports_predictor_web/logs/predictions_routes.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('predictions_routes')

# Create blueprint
predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/', methods=['GET'])
def index():
    """
    Display predictions page with filtering options
    """
    # Get filter parameters
    sport = request.args.get('sport', '')
    date_from = request.args.get('date_from', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
    date_to = request.args.get('date_to', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
    confidence = request.args.get('confidence', '')
    
    # Get available sports for filter dropdown
    sports = db.session.query(Prediction.sport).distinct().all()
    sports = [sport[0] for sport in sports]
    
    # Get available confidence levels for filter dropdown
    confidence_levels = db.session.query(Prediction.confidence).distinct().all()
    confidence_levels = [level[0] for level in confidence_levels]
    
    # Get upcoming games for context
    upcoming_games = db.session.query(Game).filter(
        Game.scheduled_time >= datetime.now(),
        Game.scheduled_time <= datetime.now() + timedelta(days=7)
    ).order_by(Game.scheduled_time).all()
    
    return render_template(
        'predictions.html',
        sports=sports,
        confidence_levels=confidence_levels,
        sport=sport,
        date_from=date_from,
        date_to=date_to,
        confidence=confidence,
        upcoming_games=upcoming_games
    )

@predictions_bp.route('/detail/<int:prediction_id>', methods=['GET'])
def prediction_detail(prediction_id):
    """
    Display detailed view of a prediction
    """
    # Get prediction
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Get player info
    player = Player.query.filter_by(id=prediction.player_id).first()
    
    # Get game info
    game = Game.query.filter_by(id=prediction.game_id).first()
    
    # Get team info
    home_team = Team.query.filter_by(name=game.home_team).first() if game else None
    away_team = Team.query.filter_by(name=game.away_team).first() if game else None
    
    # Get similar predictions (same player, stat type)
    similar_predictions = Prediction.query.filter(
        Prediction.player_id == prediction.player_id,
        Prediction.stat_type == prediction.stat_type,
        Prediction.id != prediction.id
    ).order_by(Prediction.game_date.desc()).limit(5).all()
    
    return render_template(
        'prediction_detail.html',
        prediction=prediction,
        player=player,
        game=game,
        home_team=home_team,
        away_team=away_team,
        similar_predictions=similar_predictions
    )

@predictions_bp.route('/by-game/<game_id>', methods=['GET'])
def predictions_by_game(game_id):
    """
    Display all predictions for a specific game
    """
    # Get game
    game = Game.query.filter_by(id=game_id).first_or_404()
    
    # Get predictions for this game
    predictions = Prediction.query.filter_by(game_id=game_id).all()
    
    # Get teams
    home_team = Team.query.filter_by(name=game.home_team).first()
    away_team = Team.query.filter_by(name=game.away_team).first()
    
    return render_template(
        'game_predictions.html',
        game=game,
        predictions=predictions,
        home_team=home_team,
        away_team=away_team
    )

@predictions_bp.route('/by-player/<player_id>', methods=['GET'])
def predictions_by_player(player_id):
    """
    Display all predictions for a specific player
    """
    # Get player
    player = Player.query.filter_by(id=player_id).first_or_404()
    
    # Get predictions for this player
    predictions = Prediction.query.filter_by(player_id=player_id).order_by(Prediction.game_date.desc()).all()
    
    # Get team
    team = Team.query.filter_by(name=player.team).first()
    
    return render_template(
        'player_predictions.html',
        player=player,
        predictions=predictions,
        team=team
    )

@predictions_bp.route('/by-sport/<sport>', methods=['GET'])
def predictions_by_sport(sport):
    """
    Display all predictions for a specific sport
    """
    # Get predictions for this sport
    predictions = Prediction.query.filter_by(sport=sport).order_by(Prediction.game_date.desc()).all()
    
    # Get upcoming games for this sport
    upcoming_games = Game.query.filter(
        Game.sport == sport,
        Game.scheduled_time >= datetime.now(),
        Game.scheduled_time <= datetime.now() + timedelta(days=7)
    ).order_by(Game.scheduled_time).all()
    
    return render_template(
        'sport_predictions.html',
        sport=sport,
        predictions=predictions,
        upcoming_games=upcoming_games
    )

@predictions_bp.route('/high-confidence', methods=['GET'])
def high_confidence_predictions():
    """
    Display high confidence predictions
    """
    # Get high confidence predictions for upcoming games
    predictions = Prediction.query.filter(
        Prediction.confidence == 'High',
        Prediction.game_date >= datetime.now().date(),
        Prediction.game_date <= (datetime.now() + timedelta(days=7)).date()
    ).order_by(Prediction.game_date).all()
    
    return render_template(
        'high_confidence.html',
        predictions=predictions
    )

@predictions_bp.route('/trending', methods=['GET'])
def trending_predictions():
    """
    Display trending predictions (most viewed or highest value)
    """
    # For now, just show recent predictions with high confidence
    # In a real implementation, this would track views or user interactions
    predictions = Prediction.query.filter(
        Prediction.confidence == 'High',
        Prediction.game_date >= datetime.now().date(),
        Prediction.game_date <= (datetime.now() + timedelta(days=3)).date()
    ).order_by(Prediction.over_probability.desc()).limit(10).all()
    
    return render_template(
        'trending.html',
        predictions=predictions
    )
