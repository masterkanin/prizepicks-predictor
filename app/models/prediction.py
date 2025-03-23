from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import json

# Initialize SQLAlchemy
db = SQLAlchemy()

class Prediction(db.Model):
    """Model for storing predictions"""
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    player_id = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    opponent = db.Column(db.String(100), nullable=False)
    game_date = db.Column(db.Date, nullable=False)
    game_id = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    stat_type = db.Column(db.String(50), nullable=False)
    predicted_value = db.Column(db.Float, nullable=False)
    over_probability = db.Column(db.Float, nullable=False)
    line = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.String(20), nullable=False)
    top_factors = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prediction {self.player_name} {self.stat_type}>'
    
    @property
    def top_factors_list(self):
        """Convert top_factors JSON string to list"""
        if self.top_factors:
            try:
                return json.loads(self.top_factors)
            except:
                return []
        return []

class ActualResult(db.Model):
    """Model for storing actual results"""
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    player_id = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    stat_type = db.Column(db.String(50), nullable=False)
    actual_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActualResult {self.player_name} {self.stat_type}>'

class Game(db.Model):
    """Model for storing game information"""
    id = db.Column(db.String(100), primary_key=True)
    sport = db.Column(db.String(50), nullable=False)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='scheduled')
    score_home = db.Column(db.Integer, nullable=True)
    score_away = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Game {self.home_team} vs {self.away_team}>'

class Player(db.Model):
    """Model for storing player information"""
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=True)
    jersey_number = db.Column(db.String(10), nullable=True)
    height = db.Column(db.Integer, nullable=True)  # in inches
    weight = db.Column(db.Integer, nullable=True)  # in pounds
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Player {self.name}>'

class Team(db.Model):
    """Model for storing team information"""
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=True)
    sport = db.Column(db.String(50), nullable=False)
    conference = db.Column(db.String(50), nullable=True)
    division = db.Column(db.String(50), nullable=True)
    venue = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Team {self.name}>'

class ApiKey(db.Model):
    """Model for storing API keys"""
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ApiKey {self.service}>'
