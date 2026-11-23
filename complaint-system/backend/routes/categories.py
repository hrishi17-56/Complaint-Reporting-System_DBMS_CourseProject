from flask import Blueprint, request, jsonify
import sqlite3
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.db_setup import get_db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/all', methods=['GET'])
def get_categories():
    """Get all complaint categories"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT category_id, category_name, description FROM categories ORDER BY category_id")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([dict(c) for c in categories]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get specific category"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT category_id, category_name, description FROM categories WHERE category_id = ?", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()

        if not category:
            return jsonify({"error": "Category not found"}), 404

        return jsonify(dict(category)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@categories_bp.route('/add', methods=['POST'])
def add_category():
    """Add a new category (admin only)"""
    try:
        data = request.get_json()
        category_name = data.get('category_name')
        description = data.get('description', '')

        if not category_name:
            return jsonify({"error": "Category name is required"}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO categories (category_name, description) VALUES (?, ?)",
            (category_name, description)
        )
        category_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Category added successfully!",
            "category_id": category_id
        }), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Category name already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
