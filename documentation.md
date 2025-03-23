# PrizePicks Sports Prediction System - Implementation Documentation

## Overview
This document provides comprehensive documentation for the PrizePicks sports prediction system web interface implementation. The system displays predictions from a neural network-based sports prediction model through an intuitive and interactive web interface.

## System Architecture

### Backend Components
- **Flask Web Application**: Serves the web interface and API endpoints
- **SQLAlchemy ORM**: Handles database interactions
- **Live Data Pipeline**: Integrates with Sportradar API for real-time data

### Frontend Components
- **Templates**: HTML templates for different views (Jinja2 templating)
- **JavaScript Modules**: Handle data fetching, UI interactions, and visualizations
- **CSS Styling**: Responsive design for all device sizes

## Templates
The system includes the following templates:

1. **base.html**: Base template that all other templates extend from
   - Contains common elements like navigation, footer, and script imports

2. **index.html**: Home page with featured predictions and upcoming games

3. **dashboard.html**: Performance metrics and visualization dashboard

4. **predictions.html**: Main predictions listing with filtering capabilities

5. **prediction_detail.html**: Detailed view of individual predictions
   - Shows player information, prediction details, confidence metrics
   - Includes visualization of historical performance

6. **game_predictions.html**: All predictions for a specific game
   - Groups predictions by team and player
   - Shows game information and matchup details

7. **player_predictions.html**: All predictions for a specific player
   - Shows player statistics and team information
   - Includes historical performance chart

8. **sport_predictions.html**: Sport-specific prediction views
   - Filters predictions by sport
   - Shows upcoming games for that sport

9. **high_confidence.html**: High confidence predictions
   - Displays predictions with high confidence ratings
   - Includes performance metrics for high confidence picks

10. **trending.html**: Trending predictions
    - Shows most viewed or highest value predictions
    - Includes trending players and statistics

## JavaScript Modules

### data-service.js
Handles all API calls and data processing:
- Fetches predictions, upcoming games, and performance metrics
- Implements caching to improve performance
- Provides filtering and sorting capabilities
- Handles error states and loading states

Key methods:
- `getPredictions(filters)`: Fetches predictions with optional filters
- `getUpcomingGames(filters)`: Fetches upcoming games with optional filters
- `getPerformance(filters)`: Fetches performance metrics with optional filters
- `getHighConfidencePredictions()`: Fetches high confidence predictions
- `getTrendingPredictions()`: Fetches trending predictions
- `getPlayerPredictions(playerId)`: Fetches predictions for a specific player
- `getGamePredictions(gameId)`: Fetches predictions for a specific game
- `getSportPredictions(sport)`: Fetches predictions for a specific sport

### ui-controller.js
Connects the data service to the templates and handles UI interactions:
- Initializes page-specific components
- Sets up event listeners for user interactions
- Updates UI elements with data from the data service
- Handles filtering and sorting on the client side

Key functions:
- `initializePage()`: Initializes page-specific components
- `loadFeaturedPredictions()`: Loads featured predictions for home page
- `loadUpcomingGames()`: Loads upcoming games for home page
- `loadPerformanceMetrics(filters)`: Loads performance metrics for dashboard
- `loadFilteredPredictions(filters)`: Loads predictions with filters
- `setupEventListeners()`: Sets up global event listeners
- `applyFilters(filters)`: Applies filters to current page

### chart-utilities.js
Handles chart creation and updates for visualizations:
- Creates various chart types (line, bar, etc.)
- Updates charts with new data
- Converts API data to chart-friendly formats
- Handles responsive resizing

Key methods:
- `initializePerformanceChart(canvasId, data)`: Creates performance chart
- `initializeSportPerformanceChart(canvasId, data)`: Creates sport performance chart
- `initializePlayerPerformanceChart(canvasId, data)`: Creates player performance chart
- `initializeTrendingStatsChart(canvasId, data)`: Creates trending stats chart
- `initializePredictionAccuracyChart(canvasId, data)`: Creates prediction accuracy chart
- `updateChart(canvasId, newData)`: Updates chart with new data
- `convertPerformanceToChartData(performance)`: Converts performance data to chart format
- `convertPlayerPerformanceToChartData(predictions)`: Converts player data to chart format

## API Endpoints

### Prediction Endpoints
- `GET /api/predictions`: Get all predictions with optional filters
- `GET /api/predictions/<id>`: Get a specific prediction by ID
- `GET /api/predictions/by-player/<player_id>`: Get predictions for a player
- `GET /api/predictions/by-game/<game_id>`: Get predictions for a game
- `GET /api/predictions/by-sport/<sport>`: Get predictions for a sport
- `GET /api/predictions/high-confidence`: Get high confidence predictions
- `GET /api/predictions/trending`: Get trending predictions

### Performance Endpoints
- `GET /api/performance`: Get performance metrics with optional filters
- `GET /api/performance/by-sport/<sport>`: Get performance metrics for a sport
- `GET /api/performance/by-confidence/<confidence>`: Get performance by confidence level

### Game Endpoints
- `GET /api/upcoming_games`: Get upcoming games with optional filters
- `GET /api/upcoming_games/<id>`: Get a specific game by ID
- `GET /api/upcoming_games/by-sport/<sport>`: Get upcoming games for a sport

### Utility Endpoints
- `GET /api/sports`: Get list of available sports
- `GET /api/dates`: Get list of available prediction dates

## CSS Styling
The system includes responsive CSS styling for all components:
- Card-based design for predictions and games
- Interactive hover effects and transitions
- Responsive layout for all device sizes
- Consistent color scheme and typography
- Visualization styling for charts and graphs

## Usage Instructions

### Viewing Predictions
1. Navigate to the home page to see featured predictions
2. Use the navigation menu to access different prediction views
3. Apply filters to narrow down predictions by sport, date, or confidence
4. Click on a prediction to view detailed information

### Using the Dashboard
1. Navigate to the Dashboard page
2. View overall performance metrics
3. Use filters to analyze performance by sport or date range
4. Interact with charts to explore performance data

### Exploring Player and Game Predictions
1. Click on a player name to view all predictions for that player
2. Click on a game to view all predictions for that game
3. Use the sport filter to view predictions for a specific sport

## Deployment
The system can be deployed using the following methods:

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask server: `python run.py`
4. Access the application at `http://localhost:5000`

### Production Deployment
1. Set up a production WSGI server (e.g., Gunicorn)
2. Configure a reverse proxy (e.g., Nginx)
3. Set environment variables for production settings
4. Deploy using the provided deployment script: `./deploy.sh`

## Maintenance and Updates
To maintain and update the system:

1. Update the neural network model as needed
2. Run the data pipeline to fetch new predictions: `./run_pipeline.sh`
3. Monitor performance metrics to ensure accuracy
4. Update API keys and credentials as needed

## Troubleshooting
Common issues and solutions:

1. **Missing predictions**: Ensure the data pipeline is running correctly
2. **API errors**: Check API key validity and rate limits
3. **Slow performance**: Optimize database queries and implement caching
4. **Visualization issues**: Check browser compatibility and JavaScript errors

## Conclusion
The PrizePicks sports prediction system provides a comprehensive web interface for viewing and analyzing sports predictions. The system is designed to be user-friendly, responsive, and informative, allowing users to make informed decisions based on neural network predictions.
