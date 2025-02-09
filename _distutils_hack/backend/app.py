from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simulated "database" for users (for simplicity, stored in memory)
users = {}

# Sample Course Data (Simulating a Database)
courses = [
    {"title": "Python for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
    {"title": "JavaScript Crash Course", "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c"},
    {"title": "Java Full Course", "url": "https://www.youtube.com/watch?v=grEKMHGYyns"},
    {"title": "C++ Full Course by freeCodeCamp", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
    {"title": "C Programming Full Course for Beginners by freeCodeCamp", "url": "https://www.youtube.com/watch?v=KJgsSFOSQv0"},
    {"title": "Ruby Programming Tutorial by ProgrammingKnowledge", "url": "https://www.youtube.com/watch?v=t_isvp25f6c"},
    {"title": "R Programming Tutorial for Beginners by Simplilearn", "url": "https://www.youtube.com/watch?v=8lW3hqdv7DE"}
]

# Serve the homepage (index.html) only if user is logged in
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    return render_template('index.html')

# Serve signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        
        # Simple validation (for demonstration purposes)
        if not full_name or not email or not password:
            return jsonify({"message": "Please fill in all fields"}), 400

        # Check if user already exists
        if email in users:
            return jsonify({"message": "User already exists"}), 400

        # Add the user to the "database"
        users[email] = {"full_name": full_name, "email": email, "password": password}
        
        return redirect(url_for('login_page'))
    
    return render_template('signup.html')

# Serve login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user by email
        user = users.get(email)

        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('home'))  # Redirect to the home page after login
        else:
            return jsonify({"message": "Invalid email or password"}), 400
    
    return render_template('login.html')

# API for searching courses
@app.route('/search', methods=['GET'])
def search_courses():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Ensure only logged-in users can access this route

    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({"error": "Please enter a search term."}), 400

    # Predefined course lists
    c_courses = [
        {"title": "C Programming Full Course for Beginners by freeCodeCamp", "url": "https://www.youtube.com/watch?v=KJgsSFOSQv0"},
        {"title": "C Programming Tutorial for Beginners by ProgrammingKnowledge", "url": "https://www.youtube.com/watch?v=t_isvp25f6c"},
        {"title": "C Tutorial - Full Course by freeCodeCamp", "url": "https://www.youtube.com/watch?v=2lVudUD7H1k"},
        {"title": "C Programming for Beginners - EdX", "url": "https://www.youtube.com/watch?v=jI1D3Yb1w8c"}
    ]

    python_courses = [
        {"title": "Python for Beginners by freeCodeCamp", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
        {"title": "Python Tutorial for Beginners by Programming with Mosh", "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8"},
        {"title": "Python Full Course by freeCodeCamp", "url": "https://www.youtube.com/watch?v=YYXdXT2l-Gg"},
        {"title": "Learn Python Programming by Code Academy", "url": "https://www.youtube.com/watch?v=ghTwNlgkJH0"}
    ]

    c_plus_courses = [
        {"title": "C++ Full Course by freeCodeCamp", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
        {"title": "C++ Tutorial for Beginners by ProgrammingKnowledge", "url": "https://www.youtube.com/watch?v=tjm8VJRo7Eo"},
        {"title": "Learn C++ Programming from Scratch", "url": "https://www.youtube.com/watch?v=1v_j0VEkx6M"},
        {"title": "C++ Full Course by freeCodeCamp (Updated Version)", "url": "https://www.youtube.com/watch?v=HesnLbmB7tE"}
    ]

    javascript_courses = [
        {"title": "JavaScript Crash Course by Traversy Media", "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c"},
        {"title": "JavaScript Full Course by freeCodeCamp", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg"},
        {"title": "Learn JavaScript Programming from Scratch", "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c"},
        {"title": "JavaScript Tutorial for Beginners by Mosh", "url": "https://www.youtube.com/watch?v=W6NZfCO5SIk"}
    ]

    # Handling specific queries related to certain languages
    if query == 'c':  
        filtered_courses = c_courses
    elif query == 'python':  
        filtered_courses = python_courses
    elif query == 'c++':  
        filtered_courses = c_plus_courses
    elif query == 'javascript':  
        filtered_courses = javascript_courses
    else:
        # Use OpenAI to generate suggestions if the query doesn't match any predefined courses
        prompt = f"Suggest top 5 online courses about {query}."
        try:
            openai_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
            )
            ai_suggestions = openai_response.choices[0].text.strip().split("\n")
            filtered_courses = [{"title": course, "url": "#"} for course in ai_suggestions]
        except Exception as e:
            print("Error in OpenAI API:", e)
            return jsonify({"error": "Failed to fetch AI-generated courses."}), 500

    if not filtered_courses:
        return jsonify({"error": "No courses found for your query."}), 400

    return jsonify(filtered_courses)


# Route for handling logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    return redirect(url_for('login_page'))  # Redirect to the login page after logout

if __name__ == '__main__':
    app.run(debug=True)
