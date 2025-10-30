from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    return jsonify({
        "status": "healthy",
        "pod_name": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/count', methods=['POST'])
def count_characters():
    """Main endpoint that counts characters in the provided name"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
        
        name = data['name'].strip()
        
        if not name:
            return jsonify({"error": "Name cannot be empty"}), 400
        
        # The core logic - count characters
        character_count = len(name)
        
        # Return response with pod info for demo purposes
        response = {
            "name": name,
            "length": character_count,
            "processed_by": os.environ.get('HOSTNAME', 'unknown-backend-pod'),
            "message": f"Hello {name}! Your name has {character_count} characters."
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
