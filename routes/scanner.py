import os
import joblib
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.database import save_scan, get_scan_by_id
from model.feature_extractor import extract_url_features

scanner_bp = Blueprint('scanner', __name__)

# Ensure model directory is correct relative to this file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'phishing_model.pkl')

def is_valid_url(url):
    """Basic check to ensure the URL has some structure (e.g. contains dot and some length)."""
    if not url or len(url) < 4:
        return False
    # Check if there is at least one dot in the domain part
    if '.' not in url:
        return False
    return True

@scanner_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    """Protected scan route."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if not url:
            flash('URL input cannot be empty.', 'danger')
            return render_template('scan.html')

        if not is_valid_url(url):
            flash('Invalid URL format. Please enter a valid link.', 'danger')
            return render_template('scan.html')

        try:
            # 1. Feature Extraction
            features = extract_url_features(url)
            vector = features['ml_features']

            # 2. Model Prediction
            if not os.path.exists(MODEL_PATH):
                flash('Machine learning model file is missing. Please contact the administrator.', 'danger')
                return render_template('scan.html')

            model = joblib.load(MODEL_PATH)
            # Predict class and probability
            prob = model.predict_proba([vector])[0] # [Prob(Safe), Prob(Phishing)]
            prob_phish = prob[1]

            # 3. Calculate Risk Score (0-100) & Apply simple rules
            risk_score = int(prob_phish * 100)

            # Heuristics adjustments
            if features['uses_ip'] == 'Yes':
                # Force high risk if domain is an raw IP address
                risk_score = max(risk_score, 85)
            if features['uses_shortener'] == 'Yes':
                # Boost risk for shortened URLs
                risk_score = min(risk_score + 15, 100)

            # 4. Generate Verdict
            if risk_score < 35:
                verdict = 'Safe'
            elif risk_score <= 70:
                verdict = 'Suspicious'
            else:
                verdict = 'Phishing'

            # 5. Save Scan to MySQL
            user_id = session['user_id']
            scan_id = save_scan(user_id, url, verdict, risk_score)

            if scan_id:
                return redirect(url_for('scanner.report', scan_id=scan_id))
            else:
                flash('Failed to save scan record. Please try again.', 'danger')

        except Exception as e:
            print(f"Error during scan: {e}")
            flash('An error occurred while scanning the URL.', 'danger')

    return render_template('scan.html')

@scanner_bp.route('/report/<int:scan_id>')
def report(scan_id):
    """Protected scan report route."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    scan_record = get_scan_by_id(scan_id)
    if not scan_record:
        flash('Report not found.', 'danger')
        return redirect(url_for('dashboard.index'))

    # Verify authorization
    if scan_record['user_id'] != session['user_id']:
        flash('Unauthorized access to report.', 'danger')
        return redirect(url_for('dashboard.index'))

    # Re-extract features to show granular details on the report page
    features = extract_url_features(scan_record['url'])

    return render_template('report.html', scan=scan_record, features=features)
