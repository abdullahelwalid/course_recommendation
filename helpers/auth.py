import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            # Optionally, pass the decoded payload to the wrapped function
            request.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    return decorated

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
