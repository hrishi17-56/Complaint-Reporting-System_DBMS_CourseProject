from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.db_setup import get_db

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/create', methods=['POST'])
def create_complaint():
    """Create a new complaint"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        title = data.get('title')
        description = data.get('description')

        if not all([user_id, category_id, title, description]):
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO complaints (user_id, category_id, title, description, status) 
               VALUES (?, ?, ?, ?, 'open')""",
            (user_id, category_id, title, description)
        )
        complaint_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Complaint created successfully!",
            "complaint_id": complaint_id
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/my-complaints/<int:user_id>', methods=['GET'])
def get_user_complaints(user_id):
    """Get all complaints for a user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.complaint_id, c.title, c.description, c.status, 
                   c.created_at, c.updated_at, cat.category_name
            FROM complaints c
            JOIN categories cat ON c.category_id = cat.category_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        """, (user_id,))
        
        complaints = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([dict(c) for c in complaints]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/all', methods=['GET'])
def get_all_complaints():
    """Get all complaints (admin only)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.complaint_id, c.user_id, u.name, u.email, c.title, 
                   c.description, c.status, c.created_at, c.updated_at, 
                   cat.category_name
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            JOIN categories cat ON c.category_id = cat.category_id
            ORDER BY c.created_at DESC
        """)
        
        complaints = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([dict(c) for c in complaints]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    """Get complaint details"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.complaint_id, c.user_id, u.name, u.email, c.title, 
                   c.description, c.status, c.created_at, c.updated_at, 
                   cat.category_name
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            JOIN categories cat ON c.category_id = cat.category_id
            WHERE c.complaint_id = ?
        """, (complaint_id,))
        
        complaint = cursor.fetchone()
        cursor.close()
        conn.close()

        if not complaint:
            return jsonify({"error": "Complaint not found"}), 404

        return jsonify(dict(complaint)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/<int:complaint_id>/update-status', methods=['PUT'])
def update_complaint_status(complaint_id):
    """Update complaint status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        admin_id = data.get('admin_id')
        remarks = data.get('remarks', '')

        if not new_status or not admin_id:
            return jsonify({"error": "Status and admin_id required"}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        # Get old status
        cursor.execute("SELECT status FROM complaints WHERE complaint_id = ?", (complaint_id,))
        old_complaint = cursor.fetchone()
        
        if not old_complaint:
            return jsonify({"error": "Complaint not found"}), 404
        
        old_status = old_complaint['status']
        
        # Update complaint status
        cursor.execute(
            "UPDATE complaints SET status = ?, updated_at = ? WHERE complaint_id = ?",
            (new_status, datetime.now(), complaint_id)
        )
        
        # Log the status change
        cursor.execute(
            """INSERT INTO status_logs (complaint_id, updated_by, old_status, new_status, remarks)
               VALUES (?, ?, ?, ?, ?)""",
            (complaint_id, admin_id, old_status, new_status, remarks)
        )
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Status updated successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    """Delete a complaint"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if complaint exists
        cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Complaint not found"}), 404
        
        # Delete related status logs first
        cursor.execute("DELETE FROM status_logs WHERE complaint_id = ?", (complaint_id,))
        
        # Delete complaint
        cursor.execute("DELETE FROM complaints WHERE complaint_id = ?", (complaint_id,))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Complaint deleted successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@complaints_bp.route('/stats/summary', methods=['GET'])
def get_stats():
    """Get complaint statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total complaints
        cursor.execute("SELECT COUNT(*) as total FROM complaints")
        total = cursor.fetchone()['total']
        
        # By status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM complaints 
            GROUP BY status
        """)
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # By category
        cursor.execute("""
            SELECT cat.category_name, COUNT(*) as count
            FROM complaints c
            JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name
        """)
        by_category = {row['category_name']: row['count'] for row in cursor.fetchall()}
        
        cursor.close()
        conn.close()

        return jsonify({
            "total": total,
            "by_status": by_status,
            "by_category": by_category
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
