from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)  # S3 URL
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    questionnaire_results = db.relationship('QuestionnaireResult', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)

class QuestionnaireResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    interest_prediction = db.Column(db.String(256), nullable=False)
    # Store JSON data as text in SQLite
    traits_prediction = db.Column(db.Text, nullable=False)  # Store serialized JSON
    suggested_courses = db.Column(db.Text, nullable=False)  # Store serialized JSON
    raw_answers = db.Column(db.Text, nullable=False)  # Store serialized JSON

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    issuing_school = db.Column(db.String(100), nullable=True)
    certificate_url = db.Column(db.String(300), nullable=True)  # S3 URL
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(20), nullable=False)
    prerequisites = db.Column(db.Text, nullable=True)  # Store serialized JSON
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)  # Store serialized JSON
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
