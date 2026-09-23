from flask import Flask, session, redirect, url_for
import config
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.scanner import scanner_bp
from routes.history import history_bp

# Initialize Flask application
app = Flask(__name__)

# Load configuration settings
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)
app.register_blueprint(scanner_bp)
app.register_blueprint(history_bp)

# Root route (redirects to dashboard if logged in, otherwise to login)
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
