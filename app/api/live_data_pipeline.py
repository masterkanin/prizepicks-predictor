import os
import sys
import json
import logging
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text

# Add the app directory to the path
sys.path.append('/home/ubuntu/sports_predictor_web')
from app.api.sportradar_client import SportradarAPI
from app.models.prediction import db, Prediction, ActualResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/sports_predictor_web/logs/data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_pipeline')

class LiveDataPipeline:
    """
    Pipeline for fetching live sports data from Sportradar API and preparing it for the prediction model
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the data pipeline
        
        Args:
            api_key (str): Sportradar API key. If None, will look for SPORTRADAR_API_KEY env variable
        """
        self.api = SportradarAPI(api_key)
        self.output_dir = '/home/ubuntu/sports_predictor/home/ubuntu/neural_sports_predictor/output/predictions'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Connect to database
        self.db_path = '/home/ubuntu/sports_predictor_web/app.db'
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        
        # Sports supported by our prediction model
        self.supported_sports = ['nba', 'nfl', 'mlb', 'nhl', 'ncaafb', 'ncaamb']
        
    def fetch_upcoming_games(self, days_ahead=7):
        """
        Fetch upcoming games for all supported sports
        
        Args:
            days_ahead (int): Number of days to look ahead
            
        Returns:
            dict: Dictionary of upcoming games by sport
        """
        upcoming_games = {}
        
        for sport in self.supported_sports:
            try:
                logger.info(f"Fetching upcoming games for {sport}")
                games = self.api.get_upcoming_games(sport, days=days_ahead)
                upcoming_games[sport] = games
                logger.info(f"Found {len(games)} upcoming {sport} games")
            except Exception as e:
                logger.error(f"Error fetching upcoming games for {sport}: {e}")
                upcoming_games[sport] = []
                
        return upcoming_games
    
    def fetch_player_data(self, sport, game):
        """
        Fetch player data for a specific game
        
        Args:
            sport (str): Sport code
            game (dict): Game data from the API
            
        Returns:
            dict: Dictionary of player data for home and away teams
        """
        player_data = {
            'home_team': {'players': []},
            'away_team': {'players': []}
        }
        
        try:
            # Extract team IDs
            home_team_id = game['home']['id']
            away_team_id = game['away']['id']
            
            # Get team rosters
            home_roster = self.api.get_team_roster(sport, home_team_id)
            away_roster = self.api.get_team_roster(sport, away_team_id)
            
            # Extract player data
            if home_roster and 'players' in home_roster:
                player_data['home_team']['players'] = home_roster['players']
                player_data['home_team']['name'] = home_roster.get('name', game['home'].get('name', ''))
                player_data['home_team']['id'] = home_team_id
                
            if away_roster and 'players' in away_roster:
                player_data['away_team']['players'] = away_roster['players']
                player_data['away_team']['name'] = away_roster.get('name', game['away'].get('name', ''))
                player_data['away_team']['id'] = away_team_id
                
        except Exception as e:
            logger.error(f"Error fetching player data for game {game.get('id', 'unknown')}: {e}")
            
        return player_data
    
    def fetch_player_stats(self, sport, player_id):
        """
        Fetch player statistics
        
        Args:
            sport (str): Sport code
            player_id (str): Player ID
            
        Returns:
            dict: Player statistics
        """
        try:
            return self.api.get_player_stats(sport, player_id)
        except Exception as e:
            logger.error(f"Error fetching player stats for {player_id}: {e}")
            return None
    
    def prepare_prediction_input(self, sport, game, player_data):
        """
        Prepare input data for the prediction model
        
        Args:
            sport (str): Sport code
            game (dict): Game data
            player_data (dict): Player data
            
        Returns:
            list: List of player prediction inputs
        """
        prediction_inputs = []
        
        try:
            game_date = datetime.strptime(game['scheduled'], '%Y-%m-%dT%H:%M:%S%z').date()
            game_id = game['id']
            
            # Process home team players
            for player in player_data['home_team']['players']:
                player_id = player['id']
                player_name = f"{player.get('first_name', '')} {player.get('last_name', '')}"
                
                # Get player stats
                stats = self.fetch_player_stats(sport, player_id)
                
                # Create prediction input for each relevant stat type
                stat_types = self._get_stat_types_for_sport(sport)
                
                for stat_type in stat_types:
                    # Extract relevant features for this player and stat type
                    features = self._extract_player_features(player, stats, stat_type, sport)
                    
                    # Get PrizePicks line (would come from their API in production)
                    # For now, we'll use a placeholder based on average stats
                    prizepicks_line = self._get_placeholder_line(features, stat_type, sport)
                    
                    prediction_input = {
                        'player_id': player_id,
                        'player_name': player_name,
                        'team': player_data['home_team']['name'],
                        'opponent': player_data['away_team']['name'],
                        'is_home': True,
                        'game_id': game_id,
                        'game_date': game_date.strftime('%Y-%m-%d'),
                        'sport': sport,
                        'stat_type': stat_type,
                        'prizepicks_line': prizepicks_line,
                        'features': features
                    }
                    
                    prediction_inputs.append(prediction_input)
            
            # Process away team players
            for player in player_data['away_team']['players']:
                player_id = player['id']
                player_name = f"{player.get('first_name', '')} {player.get('last_name', '')}"
                
                # Get player stats
                stats = self.fetch_player_stats(sport, player_id)
                
                # Create prediction input for each relevant stat type
                stat_types = self._get_stat_types_for_sport(sport)
                
                for stat_type in stat_types:
                    # Extract relevant features for this player and stat type
                    features = self._extract_player_features(player, stats, stat_type, sport)
                    
                    # Get PrizePicks line (would come from their API in production)
                    # For now, we'll use a placeholder based on average stats
                    prizepicks_line = self._get_placeholder_line(features, stat_type, sport)
                    
                    prediction_input = {
                        'player_id': player_id,
                        'player_name': player_name,
                        'team': player_data['away_team']['name'],
                        'opponent': player_data['home_team']['name'],
                        'is_home': False,
                        'game_id': game_id,
                        'game_date': game_date.strftime('%Y-%m-%d'),
                        'sport': sport,
                        'stat_type': stat_type,
                        'prizepicks_line': prizepicks_line,
                        'features': features
                    }
                    
                    prediction_inputs.append(prediction_input)
                    
        except Exception as e:
            logger.error(f"Error preparing prediction input for game {game.get('id', 'unknown')}: {e}")
            
        return prediction_inputs
    
    def _get_stat_types_for_sport(self, sport):
        """
        Get relevant stat types for a sport
        
        Args:
            sport (str): Sport code
            
        Returns:
            list: List of stat types
        """
        if sport == 'nba':
            return ['points', 'rebounds', 'assists', 'three_pointers']
        elif sport == 'nfl':
            return ['passing_yards', 'rushing_yards', 'receiving_yards', 'touchdowns']
        elif sport == 'mlb':
            return ['hits', 'runs', 'rbis', 'strikeouts']
        elif sport == 'nhl':
            return ['goals', 'assists', 'shots', 'saves']
        elif sport == 'ncaafb':
            return ['passing_yards', 'rushing_yards', 'receiving_yards', 'touchdowns']
        elif sport == 'ncaamb':
            return ['points', 'rebounds', 'assists', 'three_pointers']
        else:
            return []
    
    def _extract_player_features(self, player, stats, stat_type, sport):
        """
        Extract relevant features for a player and stat type
        
        Args:
            player (dict): Player data
            stats (dict): Player statistics
            stat_type (str): Type of statistic
            sport (str): Sport code
            
        Returns:
            dict: Features for prediction
        """
        # This would be a complex function in production that extracts all relevant features
        # For now, we'll use a simplified version with placeholder data
        features = {
            'player_age': player.get('age', 25),
            'player_height': player.get('height', 72),
            'player_weight': player.get('weight', 200),
            'season_avg': self._get_placeholder_season_avg(stat_type, sport),
            'last_5_avg': self._get_placeholder_last_5_avg(stat_type, sport),
            'opponent_defense_rank': self._get_placeholder_defense_rank(sport),
            'days_rest': self._get_placeholder_days_rest(),
            'is_home': player.get('is_home', True),
            'is_starter': player.get('is_starter', True)
        }
        
        return features
    
    def _get_placeholder_season_avg(self, stat_type, sport):
        """Placeholder for season average stats"""
        base_values = {
            'nba': {'points': 15.5, 'rebounds': 6.2, 'assists': 4.1, 'three_pointers': 1.8},
            'nfl': {'passing_yards': 220.5, 'rushing_yards': 45.2, 'receiving_yards': 65.3, 'touchdowns': 0.8},
            'mlb': {'hits': 1.2, 'runs': 0.7, 'rbis': 0.8, 'strikeouts': 1.5},
            'nhl': {'goals': 0.4, 'assists': 0.6, 'shots': 2.5, 'saves': 25.5},
            'ncaafb': {'passing_yards': 180.5, 'rushing_yards': 40.2, 'receiving_yards': 55.3, 'touchdowns': 0.6},
            'ncaamb': {'points': 12.5, 'rebounds': 5.2, 'assists': 3.1, 'three_pointers': 1.5}
        }
        
        # Add some randomness
        import random
        base = base_values.get(sport, {}).get(stat_type, 10.0)
        return round(base * (0.8 + 0.4 * random.random()), 1)
    
    def _get_placeholder_last_5_avg(self, stat_type, sport):
        """Placeholder for last 5 games average stats"""
        # Similar to season avg but with more variance
        season_avg = self._get_placeholder_season_avg(stat_type, sport)
        import random
        variance = 0.3  # 30% variance
        return round(season_avg * (1 - variance + 2 * variance * random.random()), 1)
    
    def _get_placeholder_defense_rank(self, sport):
        """Placeholder for opponent defense rank"""
        import random
        return random.randint(1, 30)
    
    def _get_placeholder_days_rest(self):
        """Placeholder for days rest"""
        import random
        return random.randint(1, 5)
    
    def _get_placeholder_line(self, features, stat_type, sport):
        """
        Generate a placeholder PrizePicks line based on features
        
        Args:
            features (dict): Player features
            stat_type (str): Type of statistic
            sport (str): Sport code
            
        Returns:
            float: PrizePicks line
        """
        # In production, this would come from the PrizePicks API
        # For now, we'll use the season average with a slight adjustment
        season_avg = features['season_avg']
        import random
        adjustment = random.uniform(-0.5, 0.5)
        
        # Round to nearest 0.5
        line = round((season_avg + adjustment) * 2) / 2
        return line
    
    def generate_predictions(self, prediction_inputs):
        """
        Generate predictions for player stats
        
        Args:
            prediction_inputs (list): List of prediction inputs
            
        Returns:
            list: List of predictions
        """
        predictions = []
        
        for input_data in prediction_inputs:
            try:
                # In production, this would call the actual neural network model
                # For now, we'll use a simplified placeholder model
                predicted_value = self._placeholder_prediction_model(input_data)
                
                # Calculate over probability based on predicted value and line
                line = input_data['prizepicks_line']
                over_probability = self._calculate_over_probability(predicted_value, line)
                
                # Determine confidence level
                confidence = self._determine_confidence(predicted_value, line, over_probability)
                
                # Generate top factors
                top_factors = self._generate_top_factors(input_data, predicted_value, line)
                
                prediction = {
                    'player': input_data['player_name'],
                    'player_id': input_data['player_id'],
                    'team': input_data['team'],
                    'opponent': input_data['opponent'],
                    'date': input_data['game_date'],
                    'game_id': input_data['game_id'],
                    'sport': input_data['sport'],
                    'stat': input_data['stat_type'],
                    'predicted_value': round(predicted_value, 1),
                    'over_probability': round(over_probability, 2),
                    'line': line,
                    'confidence': confidence,
                    'top_factors': top_factors
                }
                
                predictions.append(prediction)
                
            except Exception as e:
                logger.error(f"Error generating prediction: {e}")
                
        return predictions
    
    def _placeholder_prediction_model(self, input_data):
        """
        Placeholder prediction model
        
        Args:
            input_data (dict): Input data for prediction
            
        Returns:
            float: Predicted value
        """
        # In production, this would be the actual neural network model
        # For now, we'll use a simple model based on the features
        features = input_data['features']
        
        # Base prediction on season average and last 5 aver<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>