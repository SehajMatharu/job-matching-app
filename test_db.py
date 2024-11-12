from flask import Flask, request, render_template, redirect, flash, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'CEOSehaj@79',
    'database': 'job_matching'
}

# Test route to check database connection
@app.route('/test_db')
def test_db():
    try:
        # Try to establish connection
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Test users table
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()['count']
        
        # Test jobs table
        cursor.execute("SELECT COUNT(*) as count FROM jobs")
        jobs_count = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return f"""
        Database connection successful!<br>
        Number of users: {users_count}<br>
        Number of jobs: {jobs_count}<br>
        """
    
    except mysql.connector.Error as err:
        return f"""
        Database connection failed!<br>
        Error: {err}<br>
        Error Code: {err.errno}<br>
        SQLSTATE: {err.sqlstate}<br>
        """

if __name__ == '__main__':
    app.run(debug=True)