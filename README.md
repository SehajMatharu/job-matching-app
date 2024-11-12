# Job Matching Application

A Flask web application for job matching and management.

## Features

- User registration
- Job listings management
- Admin dashboard
- Database integration with MySQL

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/job-matching-app.git
cd job-matching-app
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```sql
CREATE DATABASE job_matching;
```

4. Configure database connection in `app.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'job_matching'
}
```

5. Run the application:
```bash
python app.py
```

## Usage

- Access the registration page at: `http://localhost:5000/`
- View jobs at: `http://localhost:5000/jobs`
- Admin dashboard: `http://localhost:5000/admin`
- Database check: `http://localhost:5000/check_database`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
