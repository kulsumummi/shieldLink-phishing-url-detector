from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
from database.database import register_user, get_user_by_email, get_user_by_username

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Simple regex check for email format."""
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration Route."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Input validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Uniqueness check
        if get_user_by_username(username):
            flash('Username is already taken. Please choose another.', 'danger')
            return render_template('register.html')

        if get_user_by_email(email):
            flash('Email address is already registered.', 'danger')
            return render_template('register.html')

        # Hash password and save user
        password_hash = generate_password_hash(password)
        success = register_user(username, email, password_hash)

        if success:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Database error occurred during registration. Please try again.', 'danger')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Login Route."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Both email and password are required.', 'danger')
            return render_template('login.html')

        user = get_user_by_email(email)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User Logout Route."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
