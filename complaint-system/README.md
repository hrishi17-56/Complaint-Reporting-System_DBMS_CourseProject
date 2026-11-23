
# ComplaintDesk - Complaint Management System

A full-stack complaint reporting system built with Python Flask backend and HTML/CSS/JavaScript frontend. Perfect for DBMS student projects.

## 📋 Project Overview

**Topic**: Complaint Reporting System  
**Level**: Beginner to Intermediate  
**Database**: SQLite (No external setup needed!)  
**Frontend**: HTML5, CSS3, Vanilla JavaScript  
**Backend**: Python Flask  

### Features
✅ User Registration & Login  
✅ File Complaints  
✅ Track Complaint Status  
✅ Admin Dashboard  
✅ Complaint Management (Update/Delete)  
✅ Statistics & Analytics  
✅ Responsive Design  

---

## 🗂️ Project Structure

```
complaint-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       ├── complaints.py      # Complaint management
│       └── categories.py      # Category management
├── frontend/
│   ├── index.html            # Login & Register page
│   ├── dashboard.html        # User dashboard
│   └── admin.html            # Admin panel
├── database/
│   └── db_setup.py          # Database initialization
└── README.md
```

---

## 🚀 Quick Start Guide

### Step 1: Install Python
Download and install Python 3.8+ from [python.org](https://www.python.org/)

### Step 2: Navigate to Project Directory
```bash
cd complaint-system
```

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4: Start the Server
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser
Go to: **http://localhost:5000**

---

## 👤 Test Accounts

### Admin Account (Pre-created)
After first run, create an admin user:

1. Go to Register page
2. Fill in details:
   - Name: Admin
   - Email: admin@complaint.com
   - Password: admin123

3. After registration, update the database to make it admin:
   - Open `complaint-system/database/complaint_system.db` (SQLite)
   - Or in Python:
   ```python
   import sqlite3
   conn = sqlite3.connect('database/complaint_system.db')
   cursor = conn.cursor()
   cursor.execute("UPDATE users SET role='admin' WHERE email='admin@complaint.com'")
   conn.commit()
   ```

### Regular User
- Create through the registration page

---

## 📱 Usage Guide

### For Users:
1. **Register** - Create new account
2. **Login** - Enter credentials
3. **File Complaint** - Fill title, category, description
4. **Track** - View complaint status in dashboard

### For Admin:
1. **Login** - Use admin account
2. **View Dashboard** - See all statistics
3. **View All Complaints** - See complaints from all users
4. **Update Status** - Change complaint status
5. **Add Remarks** - Add notes for each update
6. **Delete** - Remove complaints if needed

---

## 🗄️ Database Schema

### Users Table
```sql
- user_id (Primary Key)
- name
- email (Unique)
- password_hash
- role (user/admin)
- created_at
```

### Categories Table
```sql
- category_id (Primary Key)
- category_name
- description
```

### Complaints Table
```sql
- complaint_id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key)
- title
- description
- status (open/in-progress/resolved)
- created_at
- updated_at
```

### Status Logs Table
```sql
- log_id (Primary Key)
- complaint_id (Foreign Key)
- updated_by (Foreign Key)
- old_status
- new_status
- remarks
- updated_at
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/users/<id>` - Get user details

### Complaints
- `POST /api/complaints/create` - Create complaint
- `GET /api/complaints/my-complaints/<user_id>` - User's complaints
- `GET /api/complaints/all` - All complaints (admin)
- `GET /api/complaints/<id>` - Get complaint details
- `PUT /api/complaints/<id>/update-status` - Update status
- `DELETE /api/complaints/<id>` - Delete complaint
- `GET /api/complaints/stats/summary` - Statistics

### Categories
- `GET /api/categories/all` - Get all categories
- `GET /api/categories/<id>` - Get category details
- `POST /api/categories/add` - Add new category (admin)

---

## ⚠️ Troubleshooting

### "Module not found" Error
```bash
# Make sure you're in the backend directory
cd backend
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
# Then access: http://localhost:5001
```

### Frontend not loading
- Make sure you're accessing `http://localhost:5000` (not 127.0.0.1)
- Clear browser cache
- Check browser console (F12) for errors

### CORS errors
- This is usually solved, but if you still get CORS errors, check that Flask-CORS is installed:
```bash
pip install Flask-CORS
```

---

## 💾 Database Reset

To reset the database (delete all data):
```bash
# Simply delete the database file
rm database/complaint_system.db

# Restart the server - it will recreate the database
python app.py
```

---

## 📝 Notes for Students

### What You're Learning:
1. **Frontend**: HTML forms, CSS styling, JavaScript fetch API
2. **Backend**: Flask routing, Blueprint organization, CORS
3. **Database**: SQLite, SQL queries, relationships
4. **Security**: Password hashing with bcrypt
5. **Architecture**: MVC pattern, REST API design

### Customization Ideas:
1. Add email notifications
2. Add file upload for complaint attachments
3. Add user profile page
4. Add search and filter functionality
5. Add export to PDF/CSV
6. Add user comments on complaints
7. Add priority levels
8. Add SLA (Service Level Agreement) tracking

### For Submission:
- Include this entire folder
- Include database file (complaint_system.db will be auto-created)
- Include setup instructions
- No need for MySQL/MariaDB - SQLite is included!

---

## 🎓 Educational Value

This project covers:
- ✅ Database Design & Normalization
- ✅ Backend Development (Python/Flask)
- ✅ Frontend Development (HTML/CSS/JS)
- ✅ REST API Design
- ✅ Authentication & Security
- ✅ Data Validation
- ✅ Error Handling
- ✅ Responsive Design

---

## 📞 Support

If you encounter any issues:
1. Check browser console (F12 -> Console tab)
2. Check server terminal for error messages
3. Ensure Python is installed: `python --version`
4. Ensure dependencies are installed: `pip list`

---

## 📄 License

This project is provided as-is for educational purposes.

---

**Happy Coding! 🚀**
