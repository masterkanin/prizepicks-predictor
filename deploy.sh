#!/bin/bash
# Script to deploy the PrizePicks Predictor web application

# Set the working directory
cd /home/ubuntu/sports_predictor_web

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment
source venv/bin/activate

# Run the deployment script
python deploy.py

# Log completion
echo "$(date): Deployment completed" >> logs/deployment_runs.log

# Display deployment status
echo "Deployment completed. Check logs/deployment.log for details."
echo "To access the application, use the following URL:"
echo "http://$(hostname -I | awk '{print $1}'):8000"
