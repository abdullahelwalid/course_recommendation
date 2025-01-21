from email_validator import validate_email, EmailNotValidError
from flask import request, jsonify
from app import bcrypt, db
from helpers.auth import generate_token
from helpers.user import upload_to_s3
from models.models import User


def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    profile_picture = request.files.get('profile_picture')

    # Validate inputs
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required!'}), 400

    try:
        # Validate email
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Upload profile picture to S3
    profile_picture_url = None
    if profile_picture:
        try:
            profile_picture_url = upload_to_s3(profile_picture)
        except Exception as e:
            return jsonify({'message': f'Failed to upload profile picture: {str(e)}'}), 500

    # Create new user
    new_user = User(username=username, email=email, password=hashed_password, profile_picture=profile_picture_url)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'error': 'User registered successfully!'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Username or email already exists!'}), 400

def signin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required!'}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_token(user.id)
        return jsonify({
            'token': token,
            'user': {
                'username': user.username,
                'email': user.email,
                'profile_picture': user.profile_picture,
                'role': user.role
            }
        }), 200

    return jsonify({'message': 'Invalid username or password!'}), 401


def get_profile():
    user_id = request.user_id  # Retrieved from token_required decorator
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email,
        'profile_picture': user.profile_picture
    }), 200


def update_profile():
    user_id = request.user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    data = request.form
    username = data.get('username')
    email = data.get('email')
    profile_picture = request.files.get('profile_picture')

    if not username or not email:
        return jsonify({'message': 'Username and email are required!'}), 400

    user.username = username

    try:
        validate_email(email)
        user.email = email
    except Exception as e:
        return jsonify({'message': 'Invalid email format!', 'error': str(e)}), 400

    if profile_picture:
        try:
            user.profile_picture = upload_to_s3(profile_picture)
        except Exception as e:
            return jsonify({'message': 'Failed to upload profile picture!', 'error': str(e)}), 500

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update profile!', 'error': str(e)}), 500
