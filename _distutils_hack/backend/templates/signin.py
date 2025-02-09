from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database for demonstration purposes
users = []

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    # Simple validation
    if not email or not password:
        return jsonify({"message": "Please fill in both fields"}), 400
    
    # Check if user already exists
    if any(user['email'] == email for user in users):
        return jsonify({"message": "User already exists"}), 400
    
    # Save new user
    users.append({"email": email, "password": password})
    return jsonify({"message": "Signup successful!"}), 201

if __name__ == '__main__':
    app.run(debug=True)