import csv
from io import StringIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from database.database import get_user_history, delete_user_scan

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
def index():
    """Protected scan history page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    search_query = request.args.get('q', '').strip()

    # Fetch user history filtered by search query if present
    scans = get_user_history(user_id, search_query if search_query else None)

    return render_template('history.html', scans=scans, search_query=search_query)

@history_bp.route('/history/delete/<int:scan_id>', methods=['POST', 'GET'])
def delete_scan(scan_id):
    """Protected route to delete a scan history record."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    success = delete_user_scan(user_id, scan_id)

    if success:
        flash('Scan record deleted successfully.', 'success')
    else:
        flash('Failed to delete scan record or record not found.', 'danger')

    return redirect(url_for('history.index'))

@history_bp.route('/history/export')
def export_csv():
    """Export the user's scan history as a CSV file."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    scans = get_user_history(user_id)

    # Create CSV structure in memory
    si = StringIO()
    writer = csv.writer(si)
    
    # Write column headers
    writer.writerow(['Date', 'URL', 'Verdict', 'Risk Score'])
    
    # Write scan records
    for scan in scans:
        date_str = scan['scan_date'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(scan['scan_date'], 'strftime') else str(scan['scan_date'])
        writer.writerow([date_str, scan['url'], scan['prediction'], scan['risk_score']])

    output = si.getvalue()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=shieldlink_history.csv"}
    )
