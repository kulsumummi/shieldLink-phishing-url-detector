// ShieldLink URL Scanner Script

document.addEventListener('DOMContentLoaded', function() {
    const scanForm = document.getElementById('scanForm');
    const loadingContainer = document.getElementById('loadingContainer');
    const scanButton = document.getElementById('scanButton');
    const scanInput = document.getElementById('scanInput');
    const clientError = document.getElementById('clientError');

    if (scanForm) {
        scanForm.addEventListener('submit', function(e) {
            const url = scanInput.value.strip ? scanInput.value.strip() : scanInput.value.trim();

            if (!url) {
                e.preventDefault();
                showError('Please enter a URL to scan.');
                return;
            }

            if (url.length < 4 || !url.includes('.')) {
                e.preventDefault();
                showError('Please enter a valid URL (e.g. google.com or https://example.com).');
                return;
            }

            // Hide previous errors and show scanner loading spinner
            clientError.style.display = 'none';
            scanButton.disabled = true;
            scanButton.style.opacity = '0.7';
            loadingContainer.style.display = 'block';
        });
    }

    function showError(message) {
        clientError.textContent = message;
        clientError.style.display = 'block';
        // Scroll to top of form if needed
        clientError.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Auto-dismiss standard alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 500);
        }, 4000);
    });
});
