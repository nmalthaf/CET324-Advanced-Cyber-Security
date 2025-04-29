from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=20)
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=120)
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Register')

    def validate_password(self, field):
        password = field.data
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            raise ValueError("Password must contain at least one special character")

    def validate_email(self, field):
        email = field.data
        # RFC 5322 compliant email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValidationError('Invalid email address. Please check the format (e.g., user@example.com)')
        
        # Additional validation checks
        local_part, domain = email.rsplit('@', 1)
        
        if len(local_part) > 64:
            raise ValidationError('The part before @ cannot be longer than 64 characters')
            
        if len(domain) > 255:
            raise ValidationError('The domain name cannot be longer than 255 characters')
            
        if not all(part.isalnum() or part == '-' for part in domain.split('.')):
            raise ValidationError('Domain contains invalid characters')