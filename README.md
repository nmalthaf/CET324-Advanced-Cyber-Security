User Registration System

A web application for user registration with reCAPTCHA verification.

Features

- User registration with reCAPTCHA verification
- Secure password hashing
- Email and username uniqueness validation
- Modern and responsive UI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd userreg
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Run the development server:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
userreg/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── forms.py           # WTForms definitions
├── models.py          # Database models
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── instance/          # Instance-specific files (database)
```

## Security Features

- reCAPTCHA integration for form submission
- Password hashing using bcrypt
- SQLite database with proper configuration
- Form validation and sanitization

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request
