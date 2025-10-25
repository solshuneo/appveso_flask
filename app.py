from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create tables (only in production or when explicitly needed)
# with app.app_context():
#     db.create_all()

@app.route('/')
def home():
    return {
        'message': 'Thành công!',
        'status': 'success'
    }

@app.route('/api/health')
def health():
    return {
        'message': 'Ứng dụng Flask đang hoạt động bình thường',
        'status': 'healthy'
    }

# User CRUD endpoints
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data or 'phone_number' not in data:
            return jsonify({'error': 'Số điện thoại là bắt buộc'}), 400
        
        # Check if phone number already exists
        existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
        if existing_user:
            return jsonify({'error': 'Số điện thoại đã tồn tại'}), 400
        
        user = User(phone_number=data['phone_number'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Tạo user thành công',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({'user': user.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if not data or 'phone_number' not in data:
            return jsonify({'error': 'Số điện thoại là bắt buộc'}), 400
        
        # Check if new phone number already exists
        existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Số điện thoại đã tồn tại'}), 400
        
        user.phone_number = data['phone_number']
        db.session.commit()
        
        return jsonify({
            'message': 'Cập nhật user thành công',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Xóa user thành công',
            'deleted_user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
