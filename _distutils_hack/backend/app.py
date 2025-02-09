from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simulated database
users = {}

# Sample courses
courses = [
    {"title": "Python for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
    {"title": "JavaScript Crash Course", "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c"},
    {"title": "Java Full Course", "url": "https://www.youtube.com/watch?v=grEKMHGYyns"},
    {"title": "C++ Full Course", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
    {"title": "C Programming Full Course", "url": "https://www.youtube.com/watch?v=KJgsSFOSQv0"}
]

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', courses=courses)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        password = request.form['password']

        if not full_name or not email or not password:
            return jsonify({"message": "Please fill in all fields"}), 400

        if email in users:
            return jsonify({"message": "User already exists"}), 400

        users[email] = {"full_name": full_name, "email": email, "password": password}
        return redirect(url_for('login_page'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('home'))
        return jsonify({"message": "Invalid email or password"}), 400

    return render_template('login.html')

@app.route('/search', methods=['GET'])
def search_courses():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({"error": "Please enter a search term."}), 400

    filtered_courses = [course for course in courses if query in course["title"].lower()]

    if not filtered_courses:
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

    if not filtered_courses:
        return jsonify({"error": "No courses found for your query."}), 400

    return jsonify(filtered_courses)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
