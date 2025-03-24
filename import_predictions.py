import os
import json
import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create predictions table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT,
    team TEXT,
    opponent TEXT,
    sport TEXT,
    date DATE,
    stat TEXT,
    predicted_value FLOAT,
    over_probability FLOAT,
    line FLOAT,
    confidence TEXT,
    confidence_score FLOAT,
    prediction_range_low FLOAT,
    prediction_range_high FLOAT,
    top_factors TEXT
)
''')

# Clear existing predictions
cursor.execute('DELETE FROM prediction')
conn.commit()

# Generate mock predictions
sports = ['NBA', 'NFL', 'MLB', 'NHL', 'SOCCER']
players = {
    'NBA': [
        {"name": "LeBron James", "team": "LAL", "opponent": "GSW"},
        {"name": "Stephen Curry", "team": "GSW", "opponent": "LAL"},
        {"name": "Kevin Durant", "team": "PHX", "opponent": "DEN"},
        {"name": "Nikola Jokić", "team": "DEN", "opponent": "PHX"}
    ],
    'NFL': [
        {"name": "Patrick Mahomes", "team": "KC", "opponent": "SF"},
        {"name": "Travis Kelce", "team": "KC", "opponent": "SF"},
        {"name": "Brock Purdy", "team": "SF", "opponent": "KC"},
        {"name": "Christian McCaffrey", "team": "SF", "opponent": "KC"}
    ],
    'MLB': [
        {"name": "Shohei Ohtani", "team": "LAD", "opponent": "NYY"},
        {"name": "Aaron Judge", "team": "NYY", "opponent": "LAD"},
        {"name": "Mookie Betts", "team": "LAD", "opponent": "NYY"},
        {"name": "Juan Soto", "team": "NYY", "opponent": "LAD"}
    ],
    'NHL': [
        {"name": "Connor McDavid", "team": "EDM", "opponent": "TOR"},
        {"name": "Auston Matthews", "team": "TOR", "opponent": "EDM"},
        {"name": "Leon Draisaitl", "team": "EDM", "opponent": "TOR"},
        {"name": "Mitch Marner", "team": "TOR", "opponent": "EDM"}
    ],
    'SOCCER': [
        {"name": "Lionel Messi", "team": "MIA", "opponent": "NYC"},
        {"name": "Erling Haaland", "team": "MCI", "opponent": "ARS"},
        {"name": "Kylian Mbappé", "team": "RMA", "opponent": "BAR"},
        {"name": "Jude Bellingham", "team": "RMA", "opponent": "BAR"}
    ]
}

stats = {
    'NBA': ['Points', 'Rebounds', 'Assists'],
    'NFL': ['Passing Yards', 'Rushing Yards', 'Touchdowns'],
    'MLB': ['Hits', 'Home Runs', 'RBIs'],
    'NHL': ['Goals', 'Assists', 'Shots'],
    'SOCCER': ['Goals', 'Assists', 'Shots on Target']
}

import random
from datetime import datetime, timedelta

# Current date
today = datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Insert predictions
for sport in sports:
    for player in players[sport]:
        for stat in stats[sport]:
            # Generate random values
            predicted_value = round(random.uniform(10, 30), 1)
            over_probability = round(random.uniform(0.3, 0.7), 2)
            line = round(random.uniform(8, 25), 1)
            confidence_score = round(random.uniform(30, 95), 1)
            
            if confidence_score > 80:
                confidence = "High"
            elif confidence_score > 60:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            range_low = round(predicted_value * random.uniform(0.8, 0.95), 1)
            range_high = round(predicted_value * random.uniform(1.05, 1.2), 1)
            
            factors = ["Recent performance", "Team matchup", "Home court advantage", 
                      "Rest days", "Injury status", "Historical performance"]
            top_factors = "|".join(random.sample(factors, 3))
            
            # Insert for today
            cursor.execute('''
            INSERT INTO prediction (
                player, team, opponent, sport, date, stat, 
                predicted_value, over_probability, line, 
                confidence, confidence_score, 
                prediction_range_low, prediction_range_high, 
                top_factors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player["name"], player["team"], player["opponent"], 
                sport, today, stat,
                predicted_value, over_probability, line,
                confidence, confidence_score,
                range_low, range_high,
                top_factors
            ))
            
            # Insert for tomorrow (with different values)
            predicted_value = round(random.uniform(10, 30), 1)
            over_probability = round(random.uniform(0.3, 0.7), 2)
            line = round(random.uniform(8, 25), 1)
            confidence_score = round(random.uniform(30, 95), 1)
            
            if confidence_score > 80:
                confidence = "High"
            elif confidence_score > 60:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            range_low = round(predicted_value * random.uniform(0.8, 0.95), 1)
            range_high = round(predicted_value * random.uniform(1.05, 1.2), 1)
            
            top_factors = "|".join(random.sample(factors, 3))
            
            cursor.execute('''
            INSERT INTO prediction (
                player, team, opponent, sport, date, stat, 
                predicted_value, over_probability, line, 
                confidence, confidence_score, 
                prediction_range_low, prediction_range_high, 
                top_factors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player["name"], player["team"], player["opponent"], 
                sport, tomorrow, stat,
                predicted_value, over_probability, line,
                confidence, confidence_score,
                range_low, range_high,
                top_factors
            ))

# Commit changes and close connection
conn.commit()
conn.close()

print("Successfully imported predictions into the database!")
