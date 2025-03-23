#!/bin/bash

# Script to run the PrizePicks Predictor web application

# Activate virtual environment
source venv/bin/activate

# Set Flask environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize the database if it doesn't exist
if [ ! -f instance/predictions.db ]; then
    echo "Initializing database..."
    flask init-db
    echo "Database initialized."
fi

# Run the application
echo "Starting PrizePicks Predictor web application..."
python run.py
