// ShieldLink Client-Side Form Validation

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const errorContainer = document.getElementById('clientError');

            if (password !== confirmPassword) {
                e.preventDefault();
                errorContainer.textContent = 'Passwords do not match.';
                errorContainer.style.display = 'block';
            } else {
                errorContainer.style.display = 'none';
            }
        });
    }
});
