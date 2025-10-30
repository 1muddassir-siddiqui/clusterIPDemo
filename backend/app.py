from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql-service'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('MYSQL_DATABASE', 'logindb')
    )

def init_db():
    max_retries = 30
    for i in range(max_retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100)
                )
            ''')
            
            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                users_data = [
                    ('admin', 'admin123', 'Administrator'),
                    ('user', 'password', 'Regular User'),
                    ('john', 'john123', 'John Doe'),
                    ('alice', 'alice123', 'Alice Johnson')
                ]
                cursor.executemany('INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)', users_data)
                conn.commit()
            
            cursor.close()
            conn.close()
            print("✅ Database initialized successfully!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for MySQL... ({i+1}/{max_retries}): {e}")
            time.sleep(2)
    
    print("❌ Failed to connect to MySQL")
    return False

@app.route('/')
def home():
    return jsonify({
        "status": "Backend API running!",
        "message": "Backend connects to MySQL via ClusterIP",
        "endpoints": ["/login", "/health"]
    })

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"message": "Username and password required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({
                "message": f"Welcome back, {user['full_name']}!",
                "success": True,
                "user": {
                    "username": user['username'],
                    "full_name": user['full_name']
                }
            }), 200
        else:
            return jsonify({"message": "Invalid credentials", "success": False}), 401
            
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}", "success": False}), 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected via ClusterIP"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
