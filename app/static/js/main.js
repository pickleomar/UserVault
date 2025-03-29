document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initBootstrapComponents();

    // Auto-dismiss alerts
    autoDismissAlerts();

    // Form validation
    handleFormValidation();

    // AJAX Form Submissions
    handleAjaxForms();

    // Dynamic Content Loading
    handleDynamicContent();

    // Session Timeout Handling
    initSessionTimeout();

    // Dark Mode Toggle
    initDarkMode();
});

// ==================== AJAX FORM SUBMISSIONS ====================
function handleAjaxForms() {
    document.querySelectorAll('form[data-ajax="true"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';

            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const result = await response.json();
                
                if (result.redirect) {
                    window.location.href = result.redirect;
                } else if (result.message) {
                    showFlashMessage(result.message, result.category || 'success');
                }

                if (result.update) {
                    document.querySelector(result.update.selector).innerHTML = result.update.content;
                    initBootstrapComponents(); // Reinitialize components in new content
                }

            } catch (error) {
                showFlashMessage('An error occurred. Please try again.', 'danger');
            } finally {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }
        });
    });
}

// ==================== DYNAMIC CONTENT LOADING ====================
function handleDynamicContent() {
    document.querySelectorAll('a[data-dynamic-content="true"]').forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            
            const target = document.querySelector(link.dataset.target);
            const loader = document.querySelector(link.dataset.loader);
            
            if (loader) loader.classList.remove('d-none');
            
            try {
                const response = await fetch(link.href);
                const html = await response.text();
                target.innerHTML = html;
                initBootstrapComponents(); // Reinitialize components in new content
            } catch (error) {
                target.innerHTML = '<div class="alert alert-danger">Failed to load content</div>';
            } finally {
                if (loader) loader.classList.add('d-none');
            }
        });
    });
}

// ==================== SESSION TIMEOUT HANDLING ====================
function initSessionTimeout() {
    let timeout;
    const warningTime = 300000; // 5 minutes
    const logoutTime = 600000; // 10 minutes
    const modal = createTimeoutModal();

    function resetTimer() {
        clearTimeout(timeout);
        timeout = setTimeout(logoutWarning, warningTime);
    }

    function logoutWarning() {
        modal.show();
        timeout = setTimeout(logoutUser, logoutTime - warningTime);
    }

    function logoutUser() {
        window.location.href = '/logout';
    }

    function createTimeoutModal() {
        const modalHTML = `
            <div class="modal fade" id="sessionModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Session Expiring</h5>
                        </div>
                        <div class="modal-body">
                            Your session will expire in 5 minutes. Continue working to stay logged in.
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Continue</button>
                        </div>
                    </div>
                </div>
            </div>`;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        return new bootstrap.Modal(document.getElementById('sessionModal'));
    }

    // Reset timer on user activity
    ['mousemove', 'keydown', 'click'].forEach(event => {
        document.addEventListener(event, resetTimer);
    });

    resetTimer();
}

// ==================== DARK MODE TOGGLE ====================
function initDarkMode() {
    const toggle = document.getElementById('darkModeToggle');
    if (!toggle) return;

    // Load saved preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
    toggle.checked = isDarkMode;

    toggle.addEventListener('change', (e) => {
        setDarkMode(e.target.checked);
        localStorage.setItem('darkMode', e.target.checked);
    });
}

function setDarkMode(enabled) {
    document.body.classList.toggle('dark-mode', enabled);
}

// ==================== UTILITY FUNCTIONS ====================
function initBootstrapComponents() {
    // Initialize tooltips and popovers
    const tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const popovers = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    
    tooltips.map(el => new bootstrap.Tooltip(el));
    popovers.map(el => new bootstrap.Popover(el));
}

function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            new bootstrap.Alert(alert).close();
        }, 5000);
    });
}

function handleFormValidation() {
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

function showFlashMessage(message, category = 'primary') {
    const container = document.querySelector('.flash-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${category} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.prepend(alert);
    autoDismissAlerts();
}
// =================CSRF UpDATE for  ============================
document.querySelector('form[data-ajax="true"]').addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch(this.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.querySelector('[name="csrf_token"]').value
        },
        body: new URLSearchParams(new FormData(this))
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        // Show success/error message
        showAlert(data.message, data.category || 'danger');
    })
    .catch(error => {
        showAlert('An error occurred', 'danger');
    });
});

/* // =================CSRF UpDATE for login ============================

document.getElementById('login-form').addEventListener('submit', function(e) {
    if (this.dataset.ajax === "true") {
        e.preventDefault();
        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('#csrf_token').value
            },
            body: new FormData(this)
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        });
    }
}); */