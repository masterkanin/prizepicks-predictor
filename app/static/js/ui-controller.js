/**
 * UI Controller for PrizePicks Sports Prediction System
 * Handles UI interactions and connects the data service to the templates
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize UI components based on current page
    initializePage();
    
    // Setup global event listeners
    setupEventListeners();
});

/**
 * Initialize page-specific components
 */
function initializePage() {
    const currentPath = window.location.pathname;
    
    // Common initialization for all pages
    initializeNavigation();
    
    // Page-specific initialization
    if (currentPath === '/' || currentPath === '/index.html') {
        initializeHomePage();
    } else if (currentPath === '/dashboard') {
        initializeDashboard();
    } else if (currentPath === '/predictions') {
        initializePredictionsPage();
    } else if (currentPath.includes('/predictions/detail/')) {
        initializePredictionDetail();
    } else if (currentPath.includes('/predictions/by-game/')) {
        initializeGamePredictions();
    } else if (currentPath.includes('/predictions/by-player/')) {
        initializePlayerPredictions();
    } else if (currentPath.includes('/predictions/by-sport/')) {
        initializeSportPredictions();
    } else if (currentPath === '/predictions/high-confidence') {
        initializeHighConfidence();
    } else if (currentPath === '/predictions/trending') {
        initializeTrending();
    }
}

/**
 * Initialize navigation components
 */
function initializeNavigation() {
    // Highlight active navigation item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Setup dropdown menus
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            dropdownMenu.classList.toggle('show');
        });
    });
}

/**
 * Initialize home page components
 */
function initializeHomePage() {
    // Load featured predictions
    loadFeaturedPredictions();
    
    // Load upcoming games
    loadUpcomingGames();
    
    // Initialize performance charts
    initializePerformanceCharts();
}

/**
 * Initialize dashboard components
 */
function initializeDashboard() {
    // Load performance metrics
    loadPerformanceMetrics();
    
    // Initialize dashboard charts
    initializeDashboardCharts();
    
    // Setup dashboard filters
    setupDashboardFilters();
}

/**
 * Initialize predictions page components
 */
function initializePredictionsPage() {
    // Setup prediction filters
    setupPredictionFilters();
    
    // Load predictions based on current filters
    loadFilteredPredictions();
}

/**
 * Initialize prediction detail page
 */
function initializePredictionDetail() {
    // Get prediction ID from URL
    const predictionId = window.location.pathname.split('/').pop();
    
    // Load prediction details
    loadPredictionDetails(predictionId);
    
    // Initialize prediction charts
    initializePredictionCharts();
}

/**
 * Initialize game predictions page
 */
function initializeGamePredictions() {
    // Get game ID from URL
    const gameId = window.location.pathname.split('/').pop();
    
    // Load game predictions
    loadGamePredictions(gameId);
}

/**
 * Initialize player predictions page
 */
function initializePlayerPredictions() {
    // Get player ID from URL
    const playerId = window.location.pathname.split('/').pop();
    
    // Load player predictions
    loadPlayerPredictions(playerId);
    
    // Initialize player performance chart
    initializePlayerPerformanceChart();
}

/**
 * Initialize sport predictions page
 */
function initializeSportPredictions() {
    // Get sport from URL
    const sport = window.location.pathname.split('/').pop();
    
    // Load sport predictions
    loadSportPredictions(sport);
    
    // Initialize sport performance chart
    initializeSportPerformanceChart();
}

/**
 * Initialize high confidence predictions page
 */
function initializeHighConfidence() {
    // Load high confidence predictions
    loadHighConfidencePredictions();
    
    // Setup high confidence filters
    setupHighConfidenceFilters();
}

/**
 * Initialize trending predictions page
 */
function initializeTrending() {
    // Load trending predictions
    loadTrendingPredictions();
    
    // Initialize trending charts
    initializeTrendingCharts();
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Setup filter form submissions
    document.querySelectorAll('form.filter-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const filters = {};
            
            for (const [key, value] of formData.entries()) {
                filters[key] = value;
            }
            
            // Apply filters based on current page
            applyFilters(filters);
        });
    });
    
    // Setup reset filter buttons
    document.querySelectorAll('.reset-filters').forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            form.reset();
            form.dispatchEvent(new Event('submit'));
        });
    });
}

/**
 * Apply filters based on current page
 * @param {Object} filters - Filter values
 */
function applyFilters(filters) {
    const currentPath = window.location.pathname;
    
    if (currentPath === '/predictions') {
        loadFilteredPredictions(filters);
    } else if (currentPath === '/dashboard') {
        loadPerformanceMetrics(filters);
    } else if (currentPath === '/predictions/high-confidence') {
        loadHighConfidencePredictions(filters);
    } else if (currentPath === '/predictions/trending') {
        loadTrendingPredictions(filters);
    } else if (currentPath.includes('/predictions/by-sport/')) {
        const sport = window.location.pathname.split('/').pop();
        loadSportPredictions(sport, filters);
    }
}

/**
 * Load featured predictions for home page
 */
async function loadFeaturedPredictions() {
    try {
        const featuredContainer = document.getElementById('featured-predictions');
        if (!featuredContainer) return;
        
        // Show loading state
        featuredContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Get high confidence predictions
        const predictions = await dataService.getHighConfidencePredictions();
        
        // Take top 6 predictions
        const featuredPredictions = predictions.slice(0, 6);
        
        if (featuredPredictions.length === 0) {
            featuredContainer.innerHTML = '<div class="alert alert-info">No featured predictions available at this time.</div>';
            return;
        }
        
        // Build featured predictions HTML
        let html = '<div class="row">';
        
        featuredPredictions.forEach(pred => {
            html += `
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <span class="badge bg-primary">${pred.sport.toUpperCase()}</span>
                            <span class="float-end">${formatDate(pred.game_date)}</span>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">${pred.player_name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${pred.team} vs ${pred.opponent}</h6>
                            <p class="card-text">
                                <strong>${pred.stat_type}:</strong> 
                                <span class="prediction-value">${pred.predicted_value.toFixed(1)}</span>
                                <div class="progress" style="height: 5px;">
                                    <div class="progress-bar ${pred.over_probability > 0.5 ? 'bg-success' : 'bg-danger'}" 
                                        role="progressbar" 
                                        style="width: ${pred.over_probability > 0.5 ? (pred.over_probability * 100) : ((1 - pred.over_probability) * 100)}%">
                                    </div>
                                </div>
                                <small class="text-muted">${pred.over_probability > 0.5 ? 'OVER' : 'UNDER'} (${(pred.over_probability * 100).toFixed(0)}%)</small>
                            </p>
                            <p class="card-text">
                                <strong>Line:</strong> ${pred.line.toFixed(1)}
                            </p>
                            <div class="d-grid">
                                <a href="/predictions/detail/${pred.id}" class="btn btn-outline-primary">View Details</a>
                            </div>
                        </div>
                        <div class="card-footer">
                            <small class="text-muted">Confidence: 
                                <span class="badge ${pred.confidence === 'High' ? 'bg-success' : pred.confidence === 'Medium' ? 'bg-warning' : 'bg-danger'}">
                                    ${pred.confidence}
                                </span>
                            </small>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        featuredContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading featured predictions:', error);
        const featuredContainer = document.getElementById('featured-predictions');
        if (featuredContainer) {
            featuredContainer.innerHTML = '<div class="alert alert-danger">Error loading featured predictions. Please try again later.</div>';
        }
    }
}

/**
 * Load upcoming games for home page
 */
async function loadUpcomingGames() {
    try {
        const gamesContainer = document.getElementById('upcoming-games');
        if (!gamesContainer) return;
        
        // Show loading state
        gamesContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Get upcoming games
        const games = await dataService.getUpcomingGames({ days_ahead: 3 });
        
        if (games.length === 0) {
            gamesContainer.innerHTML = '<div class="alert alert-info">No upcoming games available at this time.</div>';
            return;
        }
        
        // Group games by date
        const gamesByDate = {};
        games.forEach(game => {
            const gameDate = game.scheduled.split('T')[0];
            if (!gamesByDate[gameDate]) {
                gamesByDate[gameDate] = [];
            }
            gamesByDate[gameDate].push(game);
        });
        
        // Build upcoming games HTML
        let html = '';
        
        Object.keys(gamesByDate).sort().forEach(date => {
            html += `
                <h5 class="mt-4">${formatDate(date)}</h5>
                <div class="row">
            `;
            
            gamesByDate[date].forEach(game => {
                html += `
                    <div class="col-md-4 mb-3">
                        <div class="card h-100 game-card">
                            <div class="card-header">
                                <span class="badge bg-primary">${game.sport.toUpperCase()}</span>
                                <span class="float-end">${formatTime(game.scheduled)}</span>
                            </div>
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <div class="team-info text-center">
                                        <div class="team-logo-placeholder mb-2">
                                            <i class="fas fa-shield-alt fa-2x text-primary"></i>
                                        </div>
                                        <h6>${game.home_team}</h6>
                                    </div>
                                    
                                    <div class="vs-badge">
                                        <span class="badge bg-light text-dark">VS</span>
                                    </div>
                                    
                                    <div class="team-info text-center">
                                        <div class="team-logo-placeholder mb-2">
                                            <i class="fas fa-shield-alt fa-2x text-danger"></i>
                                        </div>
                                        <h6>${game.away_team}</h6>
                                    </div>
                                </div>
                                <p class="card-text">
                                    <small class="text-muted">${game.venue || 'Venue TBD'}</small>
                                </p>
                                <div class="d-grid">
                                    <a href="/predictions/by-game/${game.id}" class="btn btn-outline-primary">View Predictions</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        });
        
        gamesContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading upcoming games:', error);
        const gamesContainer = document.getElementById('upcoming-games');
        if (gamesContainer) {
            gamesContainer.innerHTML = '<div class="alert alert-danger">Error loading upcoming games. Please try again later.</div>';
        }
    }
}

/**
 * Load performance metrics for dashboard
 * @param {Object} filters - Optional filters
 */
async function loadPerformanceMetrics(filters = {}) {
    try {
        const performanceContainer = document.getElementById('performance-metrics');
        if (!performanceContainer) return;
        
        // Show loading state
        performanceContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Get performance metrics
        const performance = await dataService.getPerformance(filters);
        
        // Build performance metrics HTML
        let html = `
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">Overall Accuracy</h5>
                            <div class="display-4 mb-2">${performance.overall_accuracy.toFixed(1)}%</div>
                            <p class="card-text text-muted">${performance.correct_predictions} / ${performance.total_predictions} correct</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">High Confidence Accuracy</h5>
                            <div class="display-4 mb-2">${performance.confidence_breakdown.high.accuracy.toFixed(1)}%</div>
                            <p class="card-text text-muted">${performance.confidence_breakdown.high.correct} / ${performance.confidence_breakdown.high.total} correct</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">Medium Confidence Accuracy</h5>
                            <div class="display-4 mb-2">${performance.confidence_breakdown.medium.accuracy.toFixed(1)}%</div>
                            <p class="card-text text-muted">${performance.confidence_breakdown.medium.correct} / ${performance.confidence_breakdown.medium.total} correct</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5>Performance by Sport</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Sport</th>
                                            <th>Total Predictions</th>
                                            <th>Correct Predictions</th>
                                            <th>Accuracy</th>
                                        </tr>
                                    </thead>
                                    <tbody>
        `;
        
        // Add sport performance rows
        Object.keys(performance.sport_accuracy).forEach(sport => {
            const sportData = performance.sport_accuracy[sport];
            html += `
                <tr>
                    <td>${sport.toUpperCase()}</td>
                    <td>${sportData.total}</td>
                    <td>${sportData.correct}</td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-success" role="progressbar" style="width: ${sportData.accuracy}%" aria-valuenow="${sportData.accuracy}" aria-valuemin="0" aria-valuemax="100">${sportData.accuracy.toFixed(1)}%</div>
                        </div>
                    </td>
                </tr>
            `;
        });
        
        html += `
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        performanceContainer.innerHTML = html;
        
        // Update charts with new data
        updatePerformanceCharts(performance);
        
    } catch (error) {
        console.error('Error loading performance metrics:', error);
        const performanceContainer = document.getElementById('performance-metrics');
        if (performanceContainer) {
            performanceContainer.innerHTML = '<div class="alert alert-danger">Error loading performance metrics. Please try again later.</div>';
        }
    }
}

/**
 * Load filtered predictions for predictions page
 * @param {Object} filters - Optional filters
 */
async function loadFilteredPredictions(filters = {}) {
    try {
        const predictionsContainer = document.getElementById('predictions-container');
        if (!predictionsContainer) return;
        
        // Show loading state
        predictionsContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Get predictions with filters
        const predictions = await dataService.getPredictions(filters);
        
        if (predictions.length === 0) {
            predictionsContainer.innerHTML = '<div class="alert alert-info">No predictions found matching your filters.</div>';
            return;
        }
        
        // Build predictions table HTML
        let html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Sport</th>
                            <th>Matchup</th>
                            <th>Date</th>
                            <th>Stat</th>
                            <th>Line</th>
                            <th>Prediction</th>
                            <th>Confidence</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        // Add prediction rows
        predictions.forEach(pred => {
            html += `
                <tr>
                    <td>
                        <a href="/predictions/by-player/${pred.player_id}">
                            ${pred.player_name}
                        </a>
                    </td>
                    <td>${pred.sport.toUpperCase()}</td>
                    <td>${pred.team} vs ${pred.opponent}</td>
                    <td>${formatDate(pred.game_date)}</td>
                    <td>${pred.stat_type}</td>
                    <td>${pred.line.toFixed(1)}</td>
                    <td>
                        <span class="prediction-value">${pred.predicted_value.toFixed(1)}</span>
                        <div class="progress" style="height: 5px;">
                            <div class="progress-bar ${pred.over_probability > 0.5 ? 'bg-success' : 'bg-danger'}" 
                                role="progressbar" 
                                style="width: ${pred.over_probability > 0.5 ? (pred.over_probability * 100) : ((1 - pred.over_probability) * 100)}%">
                            </div>
                        </div>
                        <small class="text-muted">${pred.over_probability > 0.5 ? 'OVER' : 'UNDER'} (${(pred.over_probability * 100).toFixed(0)}%)</small>
                    </td>
                    <td>
                        <span class="badge ${pred.confidence === 'High' ? 'bg-success' : pred.confidence === 'Medium' ? 'bg-warning' : 'bg-danger'}">
                            ${pred.confidence}
                        </span>
                    </td>
                    <td>
                        <a href="/predictions/detail/${pred.id}" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-eye"></i> Details
                        </a>
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        predictionsContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading filtered predictions:', error);
        const predictionsContainer = document.getElementById('predictions-container');
        if (predictionsContainer) {
            predictionsContainer.innerHTML = '<div class="alert alert-danger">Error loading predictions. Please try again later.</div>';
        }
    }
}

/**
 * Format date string to readable format
 * @param {string} dateString - Date string in ISO format
 * @returns {string} - Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * Format time string to readable format
 * @param {string} timeString - Time string in ISO format
 * @returns {string} - Formatted time string
 */
function formatTime(timeString) {
    const date = new Date(timeString);
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

/**
 * Initialize performance charts
 */
function initializePerformanceCharts() {
    // This function will be implemented to create the initial charts
    // The charts will be updated with real data when it's loaded
}

/**
 * Update performance charts with new data
 * @param {Object} performance - Performance data
 */
function updatePerformanceCharts(performance) {
    // This function will be implemented to update the charts with real data
}

/**
 * Initialize dashboard charts
 */
function initializeDashboardCharts() {
    // This function will be implemented to create the dashboard charts
}

/**
 * Setup dashboard filters
 */
function setupDashboardFilters() {
    // This function will be implemented to set up the dashboard filters
}

/**
 * Setup prediction filters
 */
function setupPredictionFilters() {
    // This function will be implemented to set up the prediction filters
}

/**
 * Load prediction details
 * @param {string} predictionId - Prediction ID
 */
function loadPredictionDetails(predictionId) {
    // This function will be implemented to load prediction details
}

/**
 * Initialize prediction charts
 */
function initializePredictionCharts() {
    // This function will be implemented to create the prediction charts
}

/**
 * Load game predictions
 * @param {string} gameId - Game ID
 */
function loadGamePredictions(gameId) {
    // This function will be implemented to load game predictions
}

/**
 * Load player predictions
 * @param {string} playerId - Player ID
 */
function loadPlayerPredictions(playerId) {
    // This function will be implemented to load player predictions
}

/**
 * Initialize player performance chart
 */
function initializePlayerPerformanceChart() {
    // This function will be implemented to create the player performance chart
}

/**
 * Load sport predictions
 * @param {string} sport - Sport code
 * @param {Object} filters - Optional filters
 */
function loadSportPredictions(sport, filters = {}) {
    // This function will be implemented to load sport predictions
}

/**
 * Initialize sport performance chart
 */
function initializeSportPerformanceChart() {
    // This function will be implemented to create the sport performance chart
}

/**
 * Load high confidence predictions
 * @param {Object} filters - Optional filters
 */
function loadHighConfidencePredictions(filters = {}) {
    // This function will be implemented to load high confidence predictions
}

/**
 * Setup high confidence filters
 */
function setupHighConfidenceFilters() {
    // This function will be implemented to set up high confidence filters
}

/**
 * Load trending predictions
 * @param {Object} filters - Optional filters
 */
function loadTrendingPredictions(filters = {}) {
    // This function will be implemented to load trending predictions
}

/**
 * Initialize trending charts
 */
function initializeTrendingCharts() {
    // This function will be implemented to create the trending charts
}
