from flask import Blueprint, request, jsonify
import bcrypt
import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.db_setup import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed, role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Account created successfully!"}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user['user_id'],
                "name": user['name'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, name, email, role, created_at FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(dict(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import sqlite3
