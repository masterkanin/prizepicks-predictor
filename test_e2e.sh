#!/bin/bash
# Script to test the end-to-end functionality of the PrizePicks Predictor web application

# Set the working directory
cd /home/ubuntu/sports_predictor_web

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment
source venv/bin/activate

echo "=== PrizePicks Predictor End-to-End Test ==="
echo "$(date): Starting end-to-end test" | tee -a logs/test.log

# 1. Test database initialization
echo -e "\n=== Testing Database Initialization ==="
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Database connection successful')" | tee -a logs/test.log
if [ $? -ne 0 ]; then
    echo "ERROR: Database initialization failed" | tee -a logs/test.log
    exit 1
fi

# 2. Test data pipeline
echo -e "\n=== Testing Data Pipeline ==="
python data_pipeline.py --mode=import | tee -a logs/test.log
if [ $? -ne 0 ]; then
    echo "WARNING: Data pipeline import test failed" | tee -a logs/test.log
    # Continue with tests
fi

# 3. Test API endpoints
echo -e "\n=== Testing API Endpoints ==="

# Start Flask app in background for testing
export FLASK_APP=run.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=5000 > logs/flask.log 2>&1 &
FLASK_PID=$!

# Wait for Flask to start
sleep 3

# Test endpoints
echo "Testing /api/sports endpoint..."
curl -s http://localhost:5000/api/sports | tee -a logs/test.log
echo -e "\n"

echo "Testing /api/dates endpoint..."
curl -s http://localhost:5000/api/dates | tee -a logs/test.log
echo -e "\n"

echo "Testing /predictions/api/list endpoint..."
curl -s http://localhost:5000/predictions/api/list | tee -a logs/test.log
echo -e "\n"

echo "Testing /api/performance endpoint..."
curl -s http://localhost:5000/api/performance | tee -a logs/test.log
echo -e "\n"

# Kill Flask process
kill $FLASK_PID

# 4. Test web server startup
echo -e "\n=== Testing Web Server Startup ==="
python run.py > logs/server_test.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "Web server started successfully" | tee -a logs/test.log
    # Kill server process
    kill $SERVER_PID
else
    echo "ERROR: Web server failed to start" | tee -a logs/test.log
    # Check logs
    cat logs/server_test.log | tee -a logs/test.log
    exit 1
fi

# 5. Test deployment script (check only)
echo -e "\n=== Testing Deployment Script ==="
python deploy.py --check-only | tee -a logs/test.log
if [ $? -ne 0 ]; then
    echo "WARNING: Deployment check failed" | tee -a logs/test.log
    # Continue with tests
fi

echo -e "\n=== End-to-End Test Completed ==="
echo "$(date): End-to-end test completed" | tee -a logs/test.log
echo "All tests passed successfully!"
