from flask import Blueprint, render_template, session, redirect, url_for
from database.database import get_user_stats

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    """Protected user dashboard route."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    username = session.get('username', 'User')

    # Fetch real statistics for this user from the MySQL database
    stats = get_user_stats(user_id)

    return render_template('dashboard.html', username=username, stats=stats)
