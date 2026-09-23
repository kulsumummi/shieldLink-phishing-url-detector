// ShieldLink Scan History Script

document.addEventListener('DOMContentLoaded', function() {
    // Attach confirmation popups to all delete actions
    const deleteForms = document.querySelectorAll('.delete-form');
    
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const userConfirmed = confirm('Are you sure you want to permanently delete this scan record from your history?');
            if (!userConfirmed) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss standard Flask alert messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 500);
        }, 4000);
    });
});
