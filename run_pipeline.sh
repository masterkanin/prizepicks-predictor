#!/bin/bash
# Script to run the data pipeline for the PrizePicks Predictor

# Set the working directory
cd /home/ubuntu/sports_predictor_web

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment
source venv/bin/activate

# Run the data pipeline in full mode
python data_pipeline.py --mode=full

# Log completion
echo "$(date): Pipeline run completed" >> logs/pipeline_runs.log
