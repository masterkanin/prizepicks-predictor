/**
 * Data Service for PrizePicks Sports Prediction System
 * Handles all API calls and data processing for the frontend
 */

class DataService {
    constructor() {
        this.baseUrl = '';
        this.cache = {
            predictions: null,
            upcomingGames: null,
            performance: null,
            sports: null,
            lastFetch: {
                predictions: null,
                upcomingGames: null,
                performance: null,
                sports: null
            }
        };
        this.cacheLifetime = 5 * 60 * 1000; // 5 minutes in milliseconds
    }

    /**
     * Fetch predictions with optional filters
     * @param {Object} filters - Optional filters (sport, date_from, date_to, confidence)
     * @returns {Promise} - Promise resolving to predictions data
     */
    async getPredictions(filters = {}) {
        // Check cache first
        if (this.cache.predictions && this.isCacheValid('predictions')) {
            // Apply filters client-side if we have cached data
            return this._filterPredictions(this.cache.predictions, filters);
        }

        // Build query string from filters
        const queryParams = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key]) {
                queryParams.append(key, filters[key]);
            }
        });

        try {
            const response = await fetch(`${this.baseUrl}/api/predictions?${queryParams.toString()}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch predictions: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Update cache
            this.cache.predictions = data.predictions;
            this.cache.lastFetch.predictions = Date.now();
            
            return data.predictions;
        } catch (error) {
            console.error('Error fetching predictions:', error);
            throw error;
        }
    }

    /**
     * Fetch upcoming games with optional filters
     * @param {Object} filters - Optional filters (sport, days_ahead)
     * @returns {Promise} - Promise resolving to upcoming games data
     */
    async getUpcomingGames(filters = {}) {
        // Check cache first
        if (this.cache.upcomingGames && this.isCacheValid('upcomingGames')) {
            // Apply filters client-side if we have cached data
            return this._filterGames(this.cache.upcomingGames, filters);
        }

        // Build query string from filters
        const queryParams = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key]) {
                queryParams.append(key, filters[key]);
            }
        });

        try {
            const response = await fetch(`${this.baseUrl}/api/upcoming_games?${queryParams.toString()}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch upcoming games: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Update cache
            this.cache.upcomingGames = data.games;
            this.cache.lastFetch.upcomingGames = Date.now();
            
            return data.games;
        } catch (error) {
            console.error('Error fetching upcoming games:', error);
            throw error;
        }
    }

    /**
     * Fetch performance metrics with optional filters
     * @param {Object} filters - Optional filters (sport, days)
     * @returns {Promise} - Promise resolving to performance data
     */
    async getPerformance(filters = {}) {
        // Check cache first
        if (this.cache.performance && this.isCacheValid('performance')) {
            return this.cache.performance;
        }

        // Build query string from filters
        const queryParams = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key]) {
                queryParams.append(key, filters[key]);
            }
        });

        try {
            const response = await fetch(`${this.baseUrl}/api/performance?${queryParams.toString()}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch performance metrics: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Update cache
            this.cache.performance = data;
            this.cache.lastFetch.performance = Date.now();
            
            return data;
        } catch (error) {
            console.error('Error fetching performance metrics:', error);
            throw error;
        }
    }

    /**
     * Fetch available sports
     * @returns {Promise} - Promise resolving to sports data
     */
    async getSports() {
        // Check cache first
        if (this.cache.sports && this.isCacheValid('sports')) {
            return this.cache.sports;
        }

        try {
            const response = await fetch(`${this.baseUrl}/api/sports`);
            if (!response.ok) {
                throw new Error(`Failed to fetch sports: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Update cache
            this.cache.sports = data;
            this.cache.lastFetch.sports = Date.now();
            
            return data;
        } catch (error) {
            console.error('Error fetching sports:', error);
            throw error;
        }
    }

    /**
     * Fetch high confidence predictions
     * @returns {Promise} - Promise resolving to high confidence predictions
     */
    async getHighConfidencePredictions() {
        try {
            const predictions = await this.getPredictions({ confidence: 'High' });
            return predictions;
        } catch (error) {
            console.error('Error fetching high confidence predictions:', error);
            throw error;
        }
    }

    /**
     * Fetch trending predictions
     * @returns {Promise} - Promise resolving to trending predictions
     */
    async getTrendingPredictions() {
        try {
            // For now, we'll use the same endpoint as high confidence
            // In a production system, this would be a separate endpoint with view tracking
            const predictions = await this.getPredictions({ 
                confidence: 'High',
                date_from: new Date().toISOString().split('T')[0],
                date_to: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            });
            
            // Sort by over_probability to get the most confident predictions
            return predictions.sort((a, b) => {
                const aProb = Math.abs(a.over_probability - 0.5);
                const bProb = Math.abs(b.over_probability - 0.5);
                return bProb - aProb;
            }).slice(0, 10);
        } catch (error) {
            console.error('Error fetching trending predictions:', error);
            throw error;
        }
    }

    /**
     * Fetch predictions for a specific player
     * @param {string} playerId - Player ID
     * @returns {Promise} - Promise resolving to player predictions
     */
    async getPlayerPredictions(playerId) {
        try {
            const predictions = await this.getPredictions();
            return predictions.filter(pred => pred.player_id === playerId);
        } catch (error) {
            console.error(`Error fetching predictions for player ${playerId}:`, error);
            throw error;
        }
    }

    /**
     * Fetch predictions for a specific game
     * @param {string} gameId - Game ID
     * @returns {Promise} - Promise resolving to game predictions
     */
    async getGamePredictions(gameId) {
        try {
            const predictions = await this.getPredictions();
            return predictions.filter(pred => pred.game_id === gameId);
        } catch (error) {
            console.error(`Error fetching predictions for game ${gameId}:`, error);
            throw error;
        }
    }

    /**
     * Fetch predictions for a specific sport
     * @param {string} sport - Sport code (e.g., 'nba', 'nfl')
     * @returns {Promise} - Promise resolving to sport predictions
     */
    async getSportPredictions(sport) {
        try {
            const predictions = await this.getPredictions({ sport });
            return predictions;
        } catch (error) {
            console.error(`Error fetching predictions for sport ${sport}:`, error);
            throw error;
        }
    }

    /**
     * Check if cache is still valid
     * @param {string} cacheKey - Cache key to check
     * @returns {boolean} - True if cache is valid, false otherwise
     */
    isCacheValid(cacheKey) {
        const lastFetch = this.cache.lastFetch[cacheKey];
        if (!lastFetch) return false;
        
        const now = Date.now();
        return (now - lastFetch) < this.cacheLifetime;
    }

    /**
     * Filter predictions based on provided filters
     * @param {Array} predictions - Predictions to filter
     * @param {Object} filters - Filters to apply
     * @returns {Array} - Filtered predictions
     * @private
     */
    _filterPredictions(predictions, filters) {
        if (!predictions) return [];
        
        return predictions.filter(pred => {
            // Filter by sport
            if (filters.sport && pred.sport !== filters.sport) {
                return false;
            }
            
            // Filter by date range
            if (filters.date_from) {
                const dateFrom = new Date(filters.date_from);
                const predDate = new Date(pred.game_date);
                if (predDate < dateFrom) {
                    return false;
                }
            }
            
            if (filters.date_to) {
                const dateTo = new Date(filters.date_to);
                const predDate = new Date(pred.game_date);
                if (predDate > dateTo) {
                    return false;
                }
            }
            
            // Filter by confidence
            if (filters.confidence && pred.confidence !== filters.confidence) {
                return false;
            }
            
            return true;
        });
    }

    /**
     * Filter games based on provided filters
     * @param {Array} games - Games to filter
     * @param {Object} filters - Filters to apply
     * @returns {Array} - Filtered games
     * @private
     */
    _filterGames(games, filters) {
        if (!games) return [];
        
        return games.filter(game => {
            // Filter by sport
            if (filters.sport && game.sport !== filters.sport) {
                return false;
            }
            
            return true;
        });
    }

    /**
     * Clear all cached data
     */
    clearCache() {
        this.cache = {
            predictions: null,
            upcomingGames: null,
            performance: null,
            sports: null,
            lastFetch: {
                predictions: null,
                upcomingGames: null,
                performance: null,
                sports: null
            }
        };
    }
}

// Create and export a singleton instance
const dataService = new DataService();
