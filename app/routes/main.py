from flask import Blueprint, render_template, request, jsonify
from app.models.prediction import Prediction
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page with performance metrics"""
    return render_template('dashboard.html')

@main_bp.route('/api/sports')
def get_sports():
    """API endpoint to get list of available sports"""
    sports = Prediction.query.with_entities(Prediction.sport).distinct().all()
    return jsonify([sport[0] for sport in sports])

@main_bp.route('/api/dates')
def get_dates():
    """API endpoint to get list of available prediction dates"""
    dates = Prediction.query.with_entities(Prediction.date).distinct().order_by(Prediction.date.desc()).all()
    return jsonify([date[0].strftime('%Y-%m-%d') for date in dates])

@main_bp.route('/api/performance')
def get_performance():
    """API endpoint to get performance metrics"""
    from sqlalchemy import func
    from app.models.prediction import ActualResult
    
    # Get date range from query parameters
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    # Get sport filter
    sport = request.args.get('sport', None)
    
    # Base query
    query = Prediction.query.join(ActualResult)
    
    # Apply filters
    if sport:
        query = query.filter(Prediction.sport == sport)
    query = query.filter(Prediction.date >= start_date)
    
    # Get total predictions
    total = query.count()
    
    # Get correct predictions (over/under)
    correct = query.filter(
        ((Prediction.over_probability > 0.5) & (ActualResult.result == 'over')) | 
        ((Prediction.over_probability <= 0.5) & (ActualResult.result == 'under'))
    ).count()
    
    # Get high confidence predictions
    high_conf = query.filter(Prediction.confidence == 'High').count()
    high_conf_correct = query.filter(
        (Prediction.confidence == 'High') & 
        (((Prediction.over_probability > 0.5) & (ActualResult.result == 'over')) | 
         ((Prediction.over_probability <= 0.5) & (ActualResult.result == 'under')))
    ).count()
    
    # Calculate accuracy
    accuracy = (correct / total) * 100 if total > 0 else 0
    high_conf_accuracy = (high_conf_correct / high_conf) * 100 if high_conf > 0 else 0
    
    # Get performance by sport
    sport_performance = []
    if not sport:
        sports = Prediction.query.with_entities(Prediction.sport).distinct().all()
        for s in sports:
            sport_name = s[0]
            sport_query = query.filter(Prediction.sport == sport_name)
            sport_total = sport_query.count()
            if sport_total > 0:
                sport_correct = sport_query.filter(
                    ((Prediction.over_probability > 0.5) & (ActualResult.result == 'over')) | 
                    ((Prediction.over_probability <= 0.5) & (ActualResult.result == 'under'))
                ).count()
                sport_accuracy = (sport_correct / sport_total) * 100
                sport_performance.append({
                    'sport': sport_name,
                    'total': sport_total,
                    'correct': sport_correct,
                    'accuracy': sport_accuracy
                })
    
    return jsonify({
        'total_predictions': total,
        'correct_predictions': correct,
        'accuracy': accuracy,
        'high_confidence_total': high_conf,
        'high_confidence_correct': high_conf_correct,
        'high_confidence_accuracy': high_conf_accuracy,
        'sport_performance': sport_performance,
        'days': days
    })
