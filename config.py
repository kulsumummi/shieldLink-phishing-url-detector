import os

# Configuration settings for ShieldLink application

# Flask application secret key
SECRET_KEY = os.environ.get('SECRET_KEY', 'shieldlink-default-secret-key-2026')

# MySQL Database connection configuration
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.environ.get('MYSQL_DB', 'shieldlink_db')

# Debug mode setting (Default False for production)
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
