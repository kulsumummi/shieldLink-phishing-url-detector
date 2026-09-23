import os
import sys
import sqlite3
import config

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False
    MySQLError = Exception

# Global state to track if we are using SQLite fallback
USE_SQLITE = False
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shieldlink.db')

def get_connection():
    """Create and return a new database connection (MySQL or SQLite fallback)."""
    global USE_SQLITE
    
    # Try MySQL first (if package is installed and not forced to SQLite)
    if HAS_MYSQL and not USE_SQLITE:
        try:
            connection = mysql.connector.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DB
            )
            return connection
        except Exception as e:
            print(f"[WARNING] MySQL connection failed: {e}. Falling back to local SQLite database.")
            USE_SQLITE = True
            
    # SQLite fallback
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        # Enable foreign key support in SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # Initialize schema tables if they don't exist
        init_sqlite_schema(conn)
        return conn
    except Exception as e:
        print(f"[ERROR] Local SQLite connection failed: {e}")
        return None

def init_sqlite_schema(conn):
    """Initialize schema tables in SQLite if they don't exist."""
    cursor = conn.cursor()
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Create scan_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    conn.commit()

def execute_query(query, params=None):
    """Execute INSERT, UPDATE, or DELETE query and commit changes."""
    connection = get_connection()
    if not connection:
        return False

    success = False
    try:
        cursor = connection.cursor()
        # Handle SQLite parameter replacement
        if USE_SQLITE:
            query = query.replace('%s', '?')
            # Skip MySQL-specific queries if any
            if "CREATE DATABASE" in query or "USE " in query:
                return True
                
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        success = True
    except Exception as e:
        print(f"Error executing query: {e}")
        if hasattr(connection, 'rollback'):
            connection.rollback()
    finally:
        connection.close()

    return success

def fetch_one(query, params=None):
    """Fetch a single row result from a query."""
    connection = get_connection()
    if not connection:
        return None

    result = None
    try:
        cursor = connection.cursor()
        # Handle SQLite parameter replacement
        if USE_SQLITE:
            query = query.replace('%s', '?')
            
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        row = cursor.fetchone()
        if row:
            # Convert SQLite row to dictionary, MySQL cursor already returns dicts
            result = dict(row) if USE_SQLITE else row
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        connection.close()

    return result

def fetch_all(query, params=None):
    """Fetch all row results from a query."""
    connection = get_connection()
    if not connection:
        return []

    results = []
    try:
        cursor = connection.cursor()
        # Handle SQLite parameter replacement
        if USE_SQLITE:
            query = query.replace('%s', '?')
            
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        rows = cursor.fetchall()
        if rows:
            results = [dict(row) for row in rows] if USE_SQLITE else rows
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        connection.close()

    return results

def get_user_by_email(email):
    """Fetch user record by email address."""
    query = "SELECT * FROM users WHERE email = %s"
    return fetch_one(query, (email,))

def get_user_by_username(username):
    """Fetch user record by username."""
    query = "SELECT * FROM users WHERE username = %s"
    return fetch_one(query, (username,))

def register_user(username, email, password_hash):
    """Insert a new user into the database."""
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    return execute_query(query, (username, email, password_hash))

def save_scan(user_id, url, prediction, risk_score):
    """Insert scan record into scan_history and return the new scan id."""
    connection = get_connection()
    if not connection:
        return None
    scan_id = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO scan_history (user_id, url, prediction, risk_score) VALUES (%s, %s, %s, %s)"
        if USE_SQLITE:
            query = query.replace('%s', '?')
            
        cursor.execute(query, (user_id, url, prediction, risk_score))
        connection.commit()
        scan_id = cursor.lastrowid
    except Exception as e:
        print(f"Error saving scan history: {e}")
        if hasattr(connection, 'rollback'):
            connection.rollback()
    finally:
        connection.close()
    return scan_id

def get_scan_by_id(scan_id):
    """Fetch scan record by scan id."""
    query = "SELECT * FROM scan_history WHERE id = %s"
    return fetch_one(query, (scan_id,))

def get_user_history(user_id, search_query=None):
    """Fetch user's scan history with optional search filters."""
    if search_query:
        query = """
            SELECT * FROM scan_history 
            WHERE user_id = %s 
              AND (url LIKE %s OR prediction LIKE %s) 
            ORDER BY scan_date DESC
        """
        like_query = f"%{search_query}%"
        return fetch_all(query, (user_id, like_query, like_query))
    else:
        query = "SELECT * FROM scan_history WHERE user_id = %s ORDER BY scan_date DESC"
        return fetch_all(query, (user_id,))

def delete_user_scan(user_id, scan_id):
    """Delete a user's scan record by id."""
    query = "DELETE FROM scan_history WHERE id = %s AND user_id = %s"
    return execute_query(query, (scan_id, user_id))

def get_user_stats(user_id):
    """Calculate aggregated stats for a user's dashboard."""
    query = """
        SELECT 
            COUNT(*) as total_scans,
            SUM(CASE WHEN prediction = 'Safe' THEN 1 ELSE 0 END) as safe_scans,
            SUM(CASE WHEN prediction = 'Suspicious' THEN 1 ELSE 0 END) as suspicious_scans,
            SUM(CASE WHEN prediction = 'Phishing' THEN 1 ELSE 0 END) as phishing_scans
        FROM scan_history 
        WHERE user_id = %s
    """
    stats = fetch_one(query, (user_id,))
    if not stats or stats['total_scans'] is None or stats['total_scans'] == 0:
        return {
            'total_scans': 0,
            'safe_scans': 0,
            'suspicious_scans': 0,
            'phishing_scans': 0
        }
    
    return {
        'total_scans': stats.get('total_scans', 0) or 0,
        'safe_scans': int(stats.get('safe_scans') or 0),
        'suspicious_scans': int(stats.get('suspicious_scans') or 0),
        'phishing_scans': int(stats.get('phishing_scans') or 0)
    }
