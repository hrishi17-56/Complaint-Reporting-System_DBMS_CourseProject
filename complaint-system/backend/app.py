from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.db_setup import init_db
from backend.routes.auth import auth_bp
from backend.routes.complaints import complaints_bp
from backend.routes.categories import categories_bp

FRONTEND_DIR = ROOT_DIR / 'frontend'
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
CORS(app)

# Initialize database on startup
init_db()

# Register route blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(complaints_bp, url_prefix='/api/complaints')
app.register_blueprint(categories_bp, url_prefix='/api/categories')

@app.route('/')
def serve_index():
    return send_from_directory(str(FRONTEND_DIR), 'index.html')

@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory(str(FRONTEND_DIR), 'dashboard.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(str(FRONTEND_DIR), 'admin.html')

@app.route('/api/health')
def health():
    return {"status": "OK", "message": "ComplaintDesk API is running!"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
