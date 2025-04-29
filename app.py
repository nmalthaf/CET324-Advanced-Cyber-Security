from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from extensions import db
from forms import RegistrationForm
from models import User
import os
from dotenv import load_dotenv
import requests
from flask_migrate import Migrate

# Load variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.config['RECAPTCHA_SITE_KEY'] = '6LePSCErAAAAAOJMNGwlDe4CBZVga9046czjsQpz'#key genrated from google recaptha (localhost)
app.config['RECAPTCHA_SECRET_KEY'] = '6LePSCErAAAAANByGuyzx_UWUUE8ny24GsdF4RWa'

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

def verify_recaptcha(response):
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': app.config['RECAPTCHA_SECRET_KEY'],
        'response': response
    }
    try:
        r = requests.post(verify_url, data=data)
        return r.json()
    except Exception as e:
        return {'success': False}

@app.route("/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            flash("Please complete the reCAPTCHA.", "danger")
            return render_template("register.html", form=form)

        if not verify_recaptcha(recaptcha_response)['success']:
            flash("reCAPTCHA verification failed. Please try again.", "danger")
            return render_template("register.html", form=form)

        # Check if username exists
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose a different one.", "danger")
            return render_template("register.html", form=form)

        # Check if email exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please use a different email.", "danger")
            return render_template("register.html", form=form)

        # Create new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("success.html")
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Please try again.", "danger")
            print(f"Error: {str(e)}")  # For debugging

    return render_template("register.html", form=form)

if __name__ == "__main__":
    with app.app_context():
        # Create the database and tables
        db.create_all()
    app.run(debug=True)