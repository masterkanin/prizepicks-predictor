"""
Generate sample prediction data for the PrizePicks sports prediction web application.
This script creates realistic sample data for multiple sports and saves it to JSON files.
"""

import os
import json
import random
from datetime import datetime, timedelta

# Define sports and their stats
SPORTS = {
    'nba': ['points', 'rebounds', 'assists', 'three_pointers', 'steals', 'blocks'],
    'nfl': ['passing_yards', 'rushing_yards', 'receiving_yards', 'touchdowns', 'receptions', 'completions'],
    'mlb': ['hits', 'runs', 'rbis', 'strikeouts', 'home_runs', 'total_bases'],
    'nhl': ['goals', 'assists', 'shots', 'saves', 'points', 'blocks'],
    'soccer': ['goals', 'assists', 'shots', 'passes', 'tackles', 'saves']
}

# Define teams for each sport
TEAMS = {
    'nba': [
        ('LAL', 'Los Angeles Lakers'), ('BOS', 'Boston Celtics'), ('GSW', 'Golden State Warriors'),
        ('MIA', 'Miami Heat'), ('CHI', 'Chicago Bulls'), ('BKN', 'Brooklyn Nets'),
        ('DAL', 'Dallas Mavericks'), ('PHX', 'Phoenix Suns'), ('DEN', 'Denver Nuggets'),
        ('MIL', 'Milwaukee Bucks'), ('PHI', 'Philadelphia 76ers'), ('TOR', 'Toronto Raptors')
    ],
    'nfl': [
        ('KC', 'Kansas City Chiefs'), ('SF', 'San Francisco 49ers'), ('DAL', 'Dallas Cowboys'),
        ('GB', 'Green Bay Packers'), ('BUF', 'Buffalo Bills'), ('BAL', 'Baltimore Ravens'),
        ('PHI', 'Philadelphia Eagles'), ('CIN', 'Cincinnati Bengals'), ('DET', 'Detroit Lions'),
        ('TB', 'Tampa Bay Buccaneers'), ('LAR', 'Los Angeles Rams'), ('NE', 'New England Patriots')
    ],
    'mlb': [
        ('NYY', 'New York Yankees'), ('LAD', 'Los Angeles Dodgers'), ('BOS', 'Boston Red Sox'),
        ('HOU', 'Houston Astros'), ('CHC', 'Chicago Cubs'), ('ATL', 'Atlanta Braves'),
        ('STL', 'St. Louis Cardinals'), ('SD', 'San Diego Padres'), ('NYM', 'New York Mets'),
        ('SF', 'San Francisco Giants'), ('PHI', 'Philadelphia Phillies'), ('TOR', 'Toronto Blue Jays')
    ],
    'nhl': [
        ('TOR', 'Toronto Maple Leafs'), ('BOS', 'Boston Bruins'), ('TB', 'Tampa Bay Lightning'),
        ('COL', 'Colorado Avalanche'), ('VGK', 'Vegas Golden Knights'), ('EDM', 'Edmonton Oilers'),
        ('NYR', 'New York Rangers'), ('CAR', 'Carolina Hurricanes'), ('FLA', 'Florida Panthers'),
        ('PIT', 'Pittsburgh Penguins'), ('WSH', 'Washington Capitals'), ('MIN', 'Minnesota Wild')
    ],
    'soccer': [
        ('MCI', 'Manchester City'), ('LIV', 'Liverpool'), ('CHE', 'Chelsea'),
        ('ARS', 'Arsenal'), ('MUN', 'Manchester United'), ('TOT', 'Tottenham Hotspur'),
        ('BAR', 'Barcelona'), ('RMA', 'Real Madrid'), ('ATM', 'Atletico Madrid'),
        ('BAY', 'Bayern Munich'), ('PSG', 'Paris Saint-Germain'), ('JUV', 'Juventus')
    ]
}

# Define players for each sport
PLAYERS = {
    'nba': [
        'LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo', 'Nikola Jokic',
        'Joel Embiid', 'Luka Doncic', 'Jayson Tatum', 'Ja Morant', 'Devin Booker',
        'Trae Young', 'Anthony Edwards', 'Damian Lillard', 'Bam Adebayo', 'Zion Williamson'
    ],
    'nfl': [
        'Patrick Mahomes', 'Josh Allen', 'Lamar Jackson', 'Joe Burrow', 'Justin Herbert',
        'Jalen Hurts', 'Dak Prescott', 'Aaron Rodgers', 'Justin Jefferson', 'Cooper Kupp',
        'Travis Kelce', 'Christian McCaffrey', 'Derrick Henry', 'Tyreek Hill', 'Davante Adams'
    ],
    'mlb': [
        'Shohei Ohtani', 'Aaron Judge', 'Mike Trout', 'Mookie Betts', 'Freddie Freeman',
        'Juan Soto', 'Vladimir Guerrero Jr.', 'Bryce Harper', 'Fernando Tatis Jr.', 'Ronald Acuña Jr.',
        'Yordan Alvarez', 'Corbin Burnes', 'Gerrit Cole', 'Jacob deGrom', 'Max Scherzer'
    ],
    'nhl': [
        'Connor McDavid', 'Auston Matthews', 'Nathan MacKinnon', 'Leon Draisaitl', 'Cale Makar',
        'Nikita Kucherov', 'Sidney Crosby', 'Alex Ovechkin', 'David Pastrnak', 'Kirill Kaprizov',
        'Mitch Marner', 'Matthew Tkachuk', 'Igor Shesterkin', 'Andrei Vasilevskiy', 'Roman Josi'
    ],
    'soccer': [
        'Lionel Messi', 'Cristiano Ronaldo', 'Kylian Mbappe', 'Erling Haaland', 'Kevin De Bruyne',
        'Mohamed Salah', 'Neymar Jr', 'Virgil van Dijk', 'Robert Lewandowski', 'Karim Benzema',
        'Luka Modric', 'Trent Alexander-Arnold', 'Harry Kane', 'Jude Bellingham', 'Vinicius Jr'
    ]
}

# Define confidence levels
CONFIDENCE_LEVELS = ['Low', 'Medium', 'High']

# Define top factors for predictions
TOP_FACTORS = {
    'nba': [
        'Recent scoring streak', 'Favorable matchup', 'Home court advantage', 
        'Playing time increase', 'Opponent defensive weakness', 'Back-to-back game',
        'Key teammate injury', 'Historical performance vs opponent', 'Rest advantage',
        'Recent shooting efficiency'
    ],
    'nfl': [
        'Favorable defensive matchup', 'Weather conditions', 'Offensive line strength',
        'Target share trend', 'Red zone opportunities', 'Game script projection',
        'Injury to key defender', 'Historical success vs opponent', 'Home field advantage',
        'Recent usage pattern'
    ],
    'mlb': [
        'Pitcher matchup advantage', 'Ballpark factors', 'Recent hitting form',
        'Weather conditions', 'Batting order position', 'Platoon advantage',
        'Historical success vs pitcher', 'Home field advantage', 'Rest days',
        'Recent power metrics'
    ],
    'nhl': [
        'Power play opportunities', 'Line matchups', 'Goalie matchup',
        'Home ice advantage', 'Back-to-back game', 'Recent form',
        'Historical performance vs opponent', 'Team defensive metrics',
        'Ice time projection', 'Special teams advantage'
    ],
    'soccer': [
        'Opponent defensive record', 'Home field advantage', 'Recent goal-scoring form',
        'Expected playing time', 'Set piece responsibility', 'Tactical matchup',
        'Historical performance vs opponent', 'Team injury situation',
        'Competition importance', 'Weather conditions'
    ]
}

def generate_sample_predictions():
    """Generate sample prediction data for all sports"""
    # Create output directory
    output_dir = '/home/ubuntu/sports_predictor/home/ubuntu/neural_sports_predictor/output/predictions'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate predictions for the last 7 days
    today = datetime.now().date()
    
    for days_ago in range(7):
        prediction_date = today - timedelta(days=days_ago)
        date_str = prediction_date.strftime('%Y-%m-%d')
        
        # Generate predictions for each sport
        for sport in SPORTS.keys():
            predictions = []
            
            # Generate 20-30 predictions per sport per day
            num_predictions = random.randint(20, 30)
            
            for _ in range(num_predictions):
                # Select random player and team
                player = random.choice(PLAYERS[sport])
                team_idx = random.randint(0, len(TEAMS[sport]) - 1)
                team_code, team_name = TEAMS[sport][team_idx]
                
                # Select random opponent (different from team)
                opponent_idx = random.randint(0, len(TEAMS[sport]) - 1)
                while opponent_idx == team_idx:
                    opponent_idx = random.randint(0, len(TEAMS[sport]) - 1)
                opponent_code, opponent_name = TEAMS[sport][opponent_idx]
                
                # Select random stat
                stat = random.choice(SPORTS[sport])
                
                # Generate prediction values
                predicted_value = round(random.uniform(10, 40), 1)
                line = round(predicted_value * random.uniform(0.85, 1.15), 1)
                over_probability = round(random.uniform(0.1, 0.9), 2)
                
                # Generate confidence
                confidence_score = round(random.uniform(30, 95), 1)
                if confidence_score >= 80:
                    confidence = 'High'
                elif confidence_score >= 60:
                    confidence = 'Medium'
                else:
                    confidence = 'Low'
                
                # Generate prediction range
                range_low = round(predicted_value * random.uniform(0.85, 0.95), 1)
                range_high = round(predicted_value * random.uniform(1.05, 1.15), 1)
                
                # Generate top factors
                num_factors = random.randint(2, 4)
                top_factors = random.sample(TOP_FACTORS[sport], num_factors)
                
                # Create prediction object
                prediction = {
                    'player': player,
                    'team': team_code,
                    'opponent': opponent_code,
                    'date': date_str,
                    'stat': stat,
                    'predicted_value': predicted_value,
                    'over_probability': over_probability,
                    'line': line,
                    'confidence': confidence,
                    'confidence_score': confidence_score,
                    'prediction_range': [range_low, range_high],
                    'top_factors': top_factors
                }
                
                predictions.append(prediction)
            
            # Save predictions to file
            filename = f"predictions_{date_str}_{sport}.json"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w') as f:
                json.dump(predictions, f, indent=2)
            
            print(f"Generated {len(predictions)} predictions for {sport} on {date_str}")

if __name__ == '__main__':
    generate_sample_predictions()
    print("Sample prediction data generation complete.")
