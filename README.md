# PrizePicks Sports Prediction System - Deployment Guide

## Overview

This document provides instructions for deploying and using the PrizePicks Sports Prediction System web application. The system uses a neural network to predict player statistics and over/under probabilities for multiple sports, including NBA, NFL, MLB, NHL, and soccer.

## System Architecture

The PrizePicks Sports Prediction System consists of the following components:

1. **Neural Network Predictor**: A deep learning model that predicts player statistics and over/under probabilities.
2. **Data Pipeline**: Automated system for collecting data, training the model, and generating predictions.
3. **Web Application**: Flask-based web interface for viewing and analyzing predictions.
4. **Database**: SQLite database for storing predictions and actual results.

## Installation Requirements

- Python 3.10 or higher
- Flask and Flask-SQLAlchemy
- Pandas, NumPy, Matplotlib, Plotly
- Gunicorn (for production deployment)
- Nginx (optional, for production deployment)

## Directory Structure

```
sports_predictor_web/
├── app/                      # Web application
│   ├── models/               # Database models
│   ├── routes/               # Route handlers
│   ├── static/               # Static files (CSS, JS)
│   ├── templates/            # HTML templates
│   └── __init__.py           # Application initialization
├── instance/                 # Instance-specific data
│   └── predictions.db        # SQLite database
├── logs/                     # Log files
├── config.py                 # Configuration settings
├── data_pipeline.py          # Data pipeline integration
├── deploy.py                 # Deployment script
├── deploy.sh                 # Deployment shell script
├── import_predictions.py     # Prediction import script
├── run.py                    # Application entry point
├── run_pipeline.sh           # Pipeline execution script
├── sample_predictions.py     # Sample data generation
├── start.sh                  # Application startup script
└── test_e2e.sh              # End-to-end test script
```

## Quick Start

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sports_predictor_web
   ```

2. Run the start script to initialize the database and start the application:
   ```
   ./start.sh
   ```

3. Access the web application at http://localhost:5000

## Deployment Options

### Development Environment

For development and testing, use the start script:

```
./start.sh
```

### Production Environment

For production deployment, use the deployment script:

```
./deploy.sh
```

This script will:
1. Check dependencies
2. Set up production configuration
3. Create systemd service (if running as root)
4. Configure Nginx (if running as root)
5. Start the application

## Data Pipeline

The data pipeline integrates the neural network predictor with the web application. To run the pipeline:

```
./run_pipeline.sh
```

### Pipeline Modes

The data pipeline can be run in different modes:

- **collect**: Collect data from various sources
- **train**: Train the neural network model
- **predict**: Generate predictions using the trained model
- **import**: Import predictions into the web application
- **full**: Run the complete pipeline (collect, train, predict, import)
- **setup-cron**: Set up a cron job for daily execution

Example:
```
python data_pipeline.py --mode=full
```

## Automated Updates

The system is configured to automatically update predictions daily. A cron job runs the data pipeline at 2 AM every day to:

1. Collect new data
2. Retrain the model
3. Generate new predictions
4. Import predictions into the web application

## Web Interface

The web interface provides the following features:

### Home Page
- Overview of the prediction system
- Links to predictions and dashboard

### Predictions Page
- View all predictions with filtering by sport, date, and confidence level
- Detailed view of individual predictions with visualization
- Over/under probabilities and confidence scores

### Dashboard
- Performance metrics and visualizations
- Accuracy by sport and confidence level
- Daily performance trends
- Top performing predictions

## API Endpoints

The web application provides the following API endpoints:

- **/api/sports**: Get list of available sports
- **/api/dates**: Get list of available prediction dates
- **/api/performance**: Get performance metrics
- **/predictions/api/list**: Get predictions with filtering
- **/predictions/api/detail/<id>**: Get detailed information about a prediction

## Troubleshooting

### Common Issues

1. **Database errors**: If the database is corrupted, delete the instance/predictions.db file and restart the application to recreate it.

2. **Missing predictions**: Ensure the data pipeline has been run successfully. Check the logs/pipeline.log file for errors.

3. **Web server not starting**: Check the logs/server_test.log file for errors. Ensure all dependencies are installed.

### Log Files

- **logs/pipeline.log**: Data pipeline execution logs
- **logs/deployment.log**: Deployment logs
- **logs/test.log**: End-to-end test logs
- **logs/server_test.log**: Web server startup logs

## Maintenance

### Database Backup

To backup the database:

```
cp instance/predictions.db instance/predictions.db.backup
```

### Updating the System

To update the system with the latest code:

1. Pull the latest changes
2. Run the deployment script
3. Restart the application

## Support

For support, please contact the development team at support@example.com.
