import os
import requests
import json
import logging
from datetime import datetime, timedelta
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/sports_predictor_web/logs/sportradar_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('sportradar_api')

class SportradarAPI:
    """
    Client for interacting with the Sportradar API to fetch live sports data
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Sportradar API client
        
        Args:
            api_key (str): Sportradar API key. If None, will look for SPORTRADAR_API_KEY env variable
        """
        self.api_key = api_key or os.environ.get('SPORTRADAR_API_KEY')
        if not self.api_key:
            logger.warning("No API key provided. Set SPORTRADAR_API_KEY environment variable or pass api_key parameter")
        
        self.base_urls = {
            'nba': 'https://api.sportradar.us/nba/trial/v8/en',
            'nfl': 'https://api.sportradar.us/nfl/official/trial/v7/en',
            'mlb': 'https://api.sportradar.us/mlb/trial/v7/en',
            'nhl': 'https://api.sportradar.us/nhl/trial/v7/en',
            'ncaafb': 'https://api.sportradar.us/ncaafb/trial/v7/en',
            'ncaamb': 'https://api.sportradar.us/ncaamb/trial/v8/en'
        }
        
        self.cache_dir = '/home/ubuntu/sports_predictor_web/cache'
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _make_request(self, url, params=None, cache_key=None, cache_ttl=3600):
        """
        Make a request to the Sportradar API with caching
        
        Args:
            url (str): Full URL for the API endpoint
            params (dict): Query parameters to include in the request
            cache_key (str): Key for caching the response
            cache_ttl (int): Time to live for cache in seconds
            
        Returns:
            dict: JSON response from the API
        """
        if not params:
            params = {}
            
        # Add API key to parameters
        params['api_key'] = self.api_key
        
        # Check cache if cache_key is provided
        if cache_key:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            if os.path.exists(cache_file):
                file_modified_time = os.path.getmtime(cache_file)
                if time.time() - file_modified_time < cache_ttl:
                    try:
                        with open(cache_file, 'r') as f:
                            logger.info(f"Using cached data for {cache_key}")
                            return json.load(f)
                    except Exception as e:
                        logger.error(f"Error reading cache file: {e}")
        
        # Make the API request
        try:
            logger.info(f"Making API request to {url}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response if cache_key is provided
            if cache_key:
                with open(cache_file, 'w') as f:
                    json.dump(data, f)
                    
            # Respect API rate limits
            time.sleep(1)
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
    
    def get_daily_schedule(self, sport, date=None):
        """
        Get the daily schedule for a sport
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            date (datetime): Date to get schedule for. Defaults to today.
            
        Returns:
            dict: Schedule data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        if date is None:
            date = datetime.now()
            
        date_str = date.strftime('%Y/%m/%d')
        url = f"{self.base_urls[sport]}/games/{date_str}/schedule.json"
        cache_key = f"{sport}_schedule_{date.strftime('%Y%m%d')}"
        
        return self._make_request(url, cache_key=cache_key)
    
    def get_team_roster(self, sport, team_id):
        """
        Get the roster for a team
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            team_id (str): Team ID
            
        Returns:
            dict: Team roster data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        url = f"{self.base_urls[sport]}/teams/{team_id}/profile.json"
        cache_key = f"{sport}_team_{team_id}"
        
        return self._make_request(url, cache_key=cache_key, cache_ttl=86400)  # Cache for 24 hours
    
    def get_player_profile(self, sport, player_id):
        """
        Get profile data for a player
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            player_id (str): Player ID
            
        Returns:
            dict: Player profile data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        url = f"{self.base_urls[sport]}/players/{player_id}/profile.json"
        cache_key = f"{sport}_player_{player_id}"
        
        return self._make_request(url, cache_key=cache_key, cache_ttl=86400)  # Cache for 24 hours
    
    def get_game_summary(self, sport, game_id):
        """
        Get summary data for a game
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            game_id (str): Game ID
            
        Returns:
            dict: Game summary data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        url = f"{self.base_urls[sport]}/games/{game_id}/summary.json"
        cache_key = f"{sport}_game_{game_id}"
        
        # Short cache TTL for game data as it changes frequently
        return self._make_request(url, cache_key=cache_key, cache_ttl=300)  # Cache for 5 minutes
    
    def get_league_standings(self, sport, season_year=None):
        """
        Get standings for a league
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            season_year (str): Season year (e.g., '2024')
            
        Returns:
            dict: League standings data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        if season_year is None:
            season_year = datetime.now().year
            
        # Different endpoints for different sports
        if sport == 'nba':
            url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/standings.json"
        elif sport == 'nfl':
            url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/standings.json"
        elif sport == 'mlb':
            url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/standings.json"
        elif sport == 'nhl':
            url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/standings.json"
        else:
            url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/standings.json"
            
        cache_key = f"{sport}_standings_{season_year}"
        
        return self._make_request(url, cache_key=cache_key, cache_ttl=86400)  # Cache for 24 hours
    
    def get_upcoming_games(self, sport, days=7):
        """
        Get upcoming games for a sport for the next N days
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            days (int): Number of days to look ahead
            
        Returns:
            list: List of upcoming games
        """
        all_games = []
        today = datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            schedule = self.get_daily_schedule(sport, date)
            
            if schedule and 'games' in schedule:
                all_games.extend(schedule['games'])
                
        return all_games
    
    def get_player_stats(self, sport, player_id, season_year=None):
        """
        Get season stats for a player
        
        Args:
            sport (str): Sport code (nba, nfl, mlb, nhl, ncaafb, ncaamb)
            player_id (str): Player ID
            season_year (str): Season year (e.g., '2024')
            
        Returns:
            dict: Player stats data
        """
        if sport not in self.base_urls:
            logger.error(f"Unsupported sport: {sport}")
            return None
            
        if season_year is None:
            season_year = datetime.now().year
            
        url = f"{self.base_urls[sport]}/seasons/{season_year}/REG/players/{player_id}/statistics.json"
        cache_key = f"{sport}_player_{player_id}_stats_{season_year}"
        
        return self._make_request(url, cache_key=cache_key, cache_ttl=86400)  # Cache for 24 hours

# Example usage
if __name__ == "__main__":
    # For testing purposes
    api = SportradarAPI()
    
    # Get today's NBA schedule
    nba_schedule = api.get_daily_schedule('nba')
    print(json.dumps(nba_schedule, indent=2))
    
    # Get upcoming NBA games
    upcoming_games = api.get_upcoming_games('nba', days=3)
    print(f"Found {len(upcoming_games)} upcoming NBA games")
