/**
 * Chart utilities for PrizePicks Sports Prediction System
 * Handles chart creation and updates for the web interface
 */

class ChartUtilities {
    constructor() {
        this.charts = {};
    }

    /**
     * Initialize performance chart on the dashboard
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Initial data for the chart
     */
    initializePerformanceChart(canvasId, data = null) {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return;

        // Default data if none provided
        const chartData = data || {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Overall Accuracy',
                    data: [65, 68, 72, 75, 73, 78],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false
                },
                {
                    label: 'High Confidence Accuracy',
                    data: [72, 75, 80, 82, 79, 85],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false
                }
            ]
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Accuracy (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * Initialize sport performance chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Initial data for the chart
     */
    initializeSportPerformanceChart(canvasId, data = null) {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return;

        // Default data if none provided
        const chartData = data || {
            labels: ['NBA', 'NFL', 'MLB', 'NHL', 'Soccer'],
            datasets: [
                {
                    label: 'Accuracy (%)',
                    data: [78, 72, 68, 75, 70],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }
            ]
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Accuracy (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Sport'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Accuracy: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * Initialize player performance chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Initial data for the chart
     */
    initializePlayerPerformanceChart(canvasId, data = null) {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return;

        // Default data if none provided
        const chartData = data || {
            labels: ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6'],
            datasets: [
                {
                    label: 'Actual',
                    data: [18, 22, 15, 25, 20, 23],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false
                },
                {
                    label: 'Predicted',
                    data: [20, 19, 18, 22, 21, 24],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: false
                },
                {
                    label: 'Line',
                    data: [19.5, 20.5, 17.5, 21.5, 20.5, 22.5],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderDash: [5, 5],
                    fill: false
                }
            ]
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Game'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * Initialize trending stats chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Initial data for the chart
     */
    initializeTrendingStatsChart(canvasId, data = null) {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return;

        // Default data if none provided
        const chartData = data || {
            labels: ['Points', 'Rebounds', 'Assists', 'Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Strikeouts', 'Hits', 'Goals'],
            datasets: [
                {
                    label: 'NBA',
                    data: [35, 28, 22, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'NFL',
                    data: [0, 0, 0, 30, 25, 20, 0, 0, 0],
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'MLB',
                    data: [0, 0, 0, 0, 0, 0, 18, 15, 0],
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'NHL',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 12],
                    backgroundColor: 'rgba(255, 206, 86, 0.5)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                }
            ]
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Stat Type'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Trending Count'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * Initialize prediction accuracy chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Initial data for the chart
     */
    initializePredictionAccuracyChart(canvasId, data = null) {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return;

        // Default data if none provided
        const chartData = data || {
            labels: ['Over', 'Under'],
            datasets: [
                {
                    label: 'Correct',
                    data: [65, 72],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(54, 162, 235, 0.7)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 1
                },
                {
                    label: 'Incorrect',
                    data: [35, 28],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 99, 132, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }
            ]
        };

        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        },
                        stacked: true
                    },
                    x: {
                        stacked: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * Update chart with new data
     * @param {string} canvasId - Canvas element ID
     * @param {Object} newData - New data for the chart
     */
    updateChart(canvasId, newData) {
        const chart = this.charts[canvasId];
        if (!chart) return;

        chart.data = newData;
        chart.update();
    }

    /**
     * Destroy chart
     * @param {string} canvasId - Canvas element ID
     */
    destroyChart(canvasId) {
        const chart = this.charts[canvasId];
        if (!chart) return;

        chart.destroy();
        delete this.charts[canvasId];
    }

    /**
     * Convert performance data to chart format
     * @param {Object} performance - Performance data
     * @returns {Object} - Chart data
     */
    convertPerformanceToChartData(performance) {
        // Extract sport names and accuracy values
        const sportNames = Object.keys(performance.sport_accuracy).map(sport => sport.toUpperCase());
        const accuracyValues = Object.values(performance.sport_accuracy).map(data => data.accuracy);

        return {
            labels: sportNames,
            datasets: [
                {
                    label: 'Accuracy (%)',
                    data: accuracyValues,
                    backgroundColor: sportNames.map((_, i) => {
                        const colors = [
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(153, 102, 255, 0.7)'
                        ];
                        return colors[i % colors.length];
                    }),
                    borderColor: sportNames.map((_, i) => {
                        const colors = [
                            'rgba(54, 162, 235, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(153, 102, 255, 1)'
                        ];
                        return colors[i % colors.length];
                    }),
                    borderWidth: 1
                }
            ]
        };
    }

    /**
     * Convert player performance data to chart format
     * @param {Array} predictions - Player predictions
     * @returns {Object} - Chart data
     */
    convertPlayerPerformanceToChartData(predictions) {
        // Sort predictions by date
        const sortedPredictions = [...predictions].sort((a, b) => {
            return new Date(a.game_date) - new Date(b.game_date);
        });

        // Extract game labels, actual values, predicted values, and lines
        const gameLabels = sortedPredictions.map(pred => {
            const date = new Date(pred.game_date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        const actualValues = sortedPredictions.map(pred => pred.actual_value || null);
        const predictedValues = sortedPredictions.map(pred => pred.predicted_value);
        const lineValues = sortedPredictions.map(pred => pred.line);

        return {
            labels: gameLabels,
            datasets: [
                {
                    label: 'Actual',
                    data: actualValues,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false
                },
                {
                    label: 'Predicted',
                    data: predictedValues,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: false
                },
                {
                    label: 'Line',
                    data: lineValues,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderDash: [5, 5],
                    fill: false
                }
            ]
        };
    }
}

// Create and export a singleton instance
const chartUtilities = new ChartUtilities();
