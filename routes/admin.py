from functools import wraps
import json
from flask import Blueprint, jsonify, request
from app import db
from helpers.auth import token_required
from models.models import User, AdminLog


admin = Blueprint('admin', __name__)

@admin.after_request
def set_cors(response):
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Dnt, Sec-Ch-Ua, Sec-Ch-Ua-Mobile, Sec-Ch-Ua-Platform'
    response.headers['Content-Type'] = 'application/json'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = User.query.get(request.user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin privileges required!'}), 403
        return f(*args, **kwargs)
    return decorated

@admin.route('/api/admin/users', methods=['GET'])
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    pagination = query.paginate(page=page, per_page=per_page)
    users = pagination.items
    
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        } for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@admin.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    if 'role' in data:
        user.role = data['role']
    
    # Log the action
    log = AdminLog(
        admin_id=request.user_id,
        action='update_user',
        details=json.dumps({
            'user_id': user_id,
            'changes': data
        })
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'})

@admin.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Log the action
    log = AdminLog(
        admin_id=request.user_id,
        action='delete_user',
        details=json.dumps({
            'user_id': user_id,
            'username': user.username
        })
    )
    
    db.session.delete(user)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})
