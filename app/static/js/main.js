// Main JavaScript file for PrizePicks Predictor web application

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add event listeners for navigation highlighting
    highlightCurrentNavItem();
});

// Function to highlight the current navigation item
function highlightCurrentNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || 
            (href === '/' && currentPath === '') || 
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Helper function to format date
function formatDate(dateString) {
    const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Helper function to format stat name
function formatStatName(stat) {
    return stat.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Helper function to get confidence class
function getConfidenceClass(confidence) {
    switch (confidence) {
        case 'High': return 'high-confidence';
        case 'Medium': return 'medium-confidence';
        case 'Low': return 'low-confidence';
        default: return '';
    }
}

// Helper function to get badge class
function getBadgeClass(confidence) {
    switch (confidence) {
        case 'High': return 'bg-success';
        case 'Medium': return 'bg-warning text-dark';
        case 'Low': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

// Helper function to get progress bar class
function getProgressBarClass(probability) {
    if (probability >= 70) return 'bg-success';
    if (probability >= 50) return 'bg-info';
    if (probability >= 30) return 'bg-warning';
    return 'bg-danger';
}

// Function to show toast notifications
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${type === 'success' ? 'bg-success text-white' : 'bg-danger text-white'}">
                <strong class="me-auto">${type === 'success' ? 'Success' : 'Error'}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}
