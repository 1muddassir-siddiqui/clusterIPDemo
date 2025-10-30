from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample employee data
employees = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "position": "Senior Developer",
        "department": "Engineering",
        "email": "alice.johnson@company.com"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "position": "Product Manager",
        "department": "Product",
        "email": "bob.smith@company.com"
    },
    {
        "id": 3,
        "name": "Carol Martinez",
        "position": "DevOps Engineer",
        "department": "Engineering",
        "email": "carol.martinez@company.com"
    },
    {
        "id": 4,
        "name": "David Lee",
        "position": "UI/UX Designer",
        "department": "Design",
        "email": "david.lee@company.com"
    },
    {
        "id": 5,
        "name": "Emma Wilson",
        "position": "Data Scientist",
        "department": "Analytics",
        "email": "emma.wilson@company.com"
    }
]

@app.route('/')
def home():
    return jsonify({
        "status": "Backend API is running!",
        "endpoints": ["/employees", "/message"]
    })

@app.route('/employees')
def get_employees():
    return jsonify(employees)

@app.route('/message')
def get_message():
    return jsonify({
        "message": "Hello from the Backend Service! 🚀",
        "status": "success"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
