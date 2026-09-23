// ShieldLink Dashboard Vanilla JS

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alert banners after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 500);
        }, 4000);
    });
});
