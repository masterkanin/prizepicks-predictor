# Railway Deployment Guide for PrizePicks Sports Prediction System

This guide provides step-by-step instructions for deploying the PrizePicks Sports Prediction System to Railway.com with live data updates every 10 minutes.

## Prerequisites
- Railway.com account
- Git installed on your local machine
- Node.js and npm installed (for Railway CLI)

## Files Added/Modified for Railway Deployment
1. **data_pipeline_scheduled.py**: Enhanced pipeline with 10-minute scheduling functionality
2. **Procfile**: Defines web and worker processes for Railway
3. **wsgi.py**: Entry point for Gunicorn web server
4. **requirements.txt**: Lists all dependencies with versions

## Deployment Steps

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/prizepicks-predictor.git
cd prizepicks-predictor
```

### 2. Install Railway CLI
```bash
npm i -g @railway/cli
```

### 3. Login to Railway
```bash
railway login
```

### 4. Initialize Railway Project
```bash
railway init
```
Follow the prompts to create a new project or link to an existing one.

### 5. Set Environment Variables
```bash
railway variables set SPORTRADAR_API_KEY=be857c22hEzoRNidkbKcAe2gz3tqhDWiETH2MJDf
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key-here
```

### 6. Deploy to Railway
```bash
railway up
```

### 7. Set Up Database
Railway will automatically provision a PostgreSQL database. The application will initialize the database tables on first run.

### 8. Access Your Deployed Application
```bash
railway domain
```
This will show you the URL where your application is deployed.

## How It Works

### Web Process
The web process runs the Flask application using Gunicorn:
```
web: gunicorn wsgi:app
```

### Worker Process
The worker process runs the data pipeline every 10 minutes:
```
worker: python data_pipeline_scheduled.py --schedule
```

### Live Data Updates
1. The worker process connects to the Sportradar API every 10 minutes
2. It fetches data for all major sports (NBA, NFL, MLB, NHL, soccer)
3. The neural network model processes this data to generate predictions
4. Predictions are saved to the database
5. The web interface displays these predictions in real-time

### Data Cleanup
The system automatically removes predictions older than 30 days to keep the database size manageable.

## Monitoring and Maintenance

### Logs
You can view logs in the Railway dashboard or using the CLI:
```bash
railway logs
```

### Updating the Application
To update your application:
1. Make changes to your code
2. Commit changes to Git
3. Push to Railway:
```bash
railway up
```

### Scaling
Railway automatically scales your application based on usage. You can adjust scaling settings in the Railway dashboard.

## Troubleshooting

### API Key Issues
If you see "No API key provided" warnings, verify your SPORTRADAR_API_KEY environment variable is set correctly.

### Database Connection Issues
Railway may occasionally change database connection strings. If you encounter database connection issues, check your Railway dashboard for updated connection information.

### Worker Process Not Running
If the worker process isn't running, check the logs for errors and ensure your Procfile is correctly formatted.
