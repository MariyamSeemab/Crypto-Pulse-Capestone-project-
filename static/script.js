// Global JavaScript for CryptoPulse

// Price alert management
class PriceAlertManager {
    constructor() {
        this.alerts = JSON.parse(localStorage.getItem('priceAlerts') || '{}');
        this.currentPrices = {};
    }

    setAlert(coin, price, type) {
        this.alerts[coin] = { price: parseFloat(price), type };
        localStorage.setItem('priceAlerts', JSON.stringify(this.alerts));
    }

    checkAlerts(prices) {
        Object.keys(this.alerts).forEach(coin => {
            if (prices[coin]) {
                const alert = this.alerts[coin];
                const currentPrice = prices[coin].usd;
                const alertTriggered = 
                    (alert.type === 'above' && currentPrice >= alert.price) ||
                    (alert.type === 'below' && currentPrice <= alert.price);

                if (alertTriggered) {
                    this.triggerAlert(coin, currentPrice, alert);
                }
            }
        });
    }

    triggerAlert(coin, price, alert) {
        // Visual alert
        const row = document.querySelector(`[data-coin="${coin}"]`).closest('tr');
        if (row) {
            row.classList.add(alert.type === 'above' ? 'price-alert-high' : 'price-alert-low');
            setTimeout(() => {
                row.classList.remove('price-alert-high', 'price-alert-low');
            }, 3000);
        }

        // Browser notification (if permission granted)
        if (Notification.permission === 'granted') {
            new Notification(`Price Alert: ${coin.toUpperCase()}`, {
                body: `Price is now $${price.toLocaleString()} (${alert.type} $${alert.price})`,
                icon: '/static/favicon.ico'
            });
        }
    }

    getAlert(coin) {
        return this.alerts[coin];
    }

    removeAlert(coin) {
        delete this.alerts[coin];
        localStorage.setItem('priceAlerts', JSON.stringify(this.alerts));
    }
}

// Initialize alert manager
const alertManager = new PriceAlertManager();

// Request notification permission on page load
document.addEventListener('DOMContentLoaded', function() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
});

// Utility functions
function formatPrice(price) {
    if (price >= 1) {
        return price.toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    } else {
        return price.toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 4,
            maximumFractionDigits: 6
        });
    }
}

function formatPercentage(percentage) {
    const sign = percentage >= 0 ? '+' : '';
    return `${sign}${percentage.toFixed(2)}%`;
}

// Enhanced search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const searchTerm = e.target.value.toLowerCase();
            filterTable(searchTerm);
        }, 300));
    }
}

function filterTable(searchTerm) {
    const rows = document.querySelectorAll('#pricesTableBody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const coinName = row.querySelector('.coin-name').textContent.toLowerCase();
        const isVisible = coinName.includes(searchTerm);
        row.style.display = isVisible ? '' : 'none';
        if (isVisible) visibleCount++;
    });

    // Show "no results" message if needed
    updateNoResultsMessage(visibleCount === 0 && searchTerm.length > 0);
}

function updateNoResultsMessage(show) {
    let noResultsRow = document.getElementById('noResultsRow');
    
    if (show && !noResultsRow) {
        const tbody = document.getElementById('pricesTableBody');
        noResultsRow = document.createElement('tr');
        noResultsRow.id = 'noResultsRow';
        noResultsRow.innerHTML = '<td colspan="5" class="text-center text-muted">No coins found matching your search.</td>';
        tbody.appendChild(noResultsRow);
    } else if (!show && noResultsRow) {
        noResultsRow.remove();
    }
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Loading state management
function setLoadingState(element, isLoading) {
    if (isLoading) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    } else {
        element.classList.remove('loading');
        element.style.pointerEvents = 'auto';
    }
}

// Error handling
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Success message
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 3000);
}

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Export for use in templates
window.alertManager = alertManager;
window.formatPrice = formatPrice;
window.formatPercentage = formatPercentage;
window.showError = showError;
window.showSuccess = showSuccess;