from flask import Flask, request, render_template, redirect, flash, url_for
import mysql.connector
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'CEOSehaj@79',
    'database': 'job_matching'
}

def get_db_connection():
    """Create and return a new database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def validate_user_input(name, dob, gender, experience):
    """Validate user input data"""
    errors = []
    
    if not name or len(name) > 100:
        errors.append("Name is required and must be less than 100 characters")
    
    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        if dob_date > datetime.now():
            errors.append("Date of birth cannot be in the future")
    except ValueError:
        errors.append("Invalid date format")
    
    if not gender or gender.lower() not in ['male', 'female', 'other']:
        errors.append("Gender must be 'male', 'female', or 'other'")
    
    if not experience:
        errors.append("Experience is required")
    
    return errors

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dob = request.form.get('dob', '')
        gender = request.form.get('gender', '').strip()
        experience = request.form.get('experience', '').strip()
        
        # Validate input
        errors = validate_user_input(name, dob, gender, experience)
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert user data
            cursor.execute(
                "INSERT INTO users (name, dob, gender, experience) VALUES (%s, %s, %s, %s)",
                (name, dob, gender, experience)
            )
            conn.commit()
            
            flash('Registration successful!', 'success')
            return redirect(url_for('jobs'))
            
        except mysql.connector.Error as err:
            flash(f"An error occurred: {err}", 'error')
            return render_template('register.html')
            
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
    
    return render_template('register.html')

@app.route('/jobs')
def jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all jobs with their requirements
        cursor.execute("""
            SELECT id, title, description, requirements 
            FROM jobs 
            ORDER BY id DESC
        """)
        jobs = cursor.fetchall()
        
        return render_template('jobs.html', jobs=jobs)
        
    except mysql.connector.Error as err:
        flash(f"An error occurred: {err}", 'error')
        return redirect(url_for('register'))
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# API endpoint to add jobs (for admin use)
@app.route('/add_job', methods=['POST'])
def add_job():
    if not request.is_json:
        return {'error': 'Content-Type must be application/json'}, 400
        
    data = request.json
    required_fields = ['title', 'description', 'requirements']
    
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO jobs (title, description, requirements) VALUES (%s, %s, %s)",
            (data['title'], data['description'], data['requirements'])
        )
        conn.commit()
        
        return {'message': 'Job added successfully', 'id': cursor.lastrowid}, 201
        
    except mysql.connector.Error as err:
        return {'error': str(err)}, 500
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)







    # Add these routes to your existing app.py

from flask import jsonify

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
        jobs = cursor.fetchall()
        
        return jsonify(jobs)
        
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Job not found'}), 404
            
        return jsonify({'message': 'Job deleted successfully'})
        
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

@app.route('/check_database')
def check_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all users
        cursor.execute("""
            SELECT id, name, dob, gender, experience, created_at 
            FROM users 
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        
        # Get all jobs
        cursor.execute("""
            SELECT id, title, description, requirements, created_at 
            FROM jobs 
            ORDER BY created_at DESC
        """)
        jobs = cursor.fetchall()
        
        return render_template('database_check.html', users=users, jobs=jobs)
        
    except mysql.connector.Error as err:
        return f"Database Error: {err}", 500
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()