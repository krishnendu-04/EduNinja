from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS globally

@app.route('/')
def home():
    return jsonify({"message": "Welcome to EduNinja API!"})

@app.route('/courses', methods=['GET'])
def get_courses():
    print("🔥 GET /courses route hit!")  # Debug log

    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, thumbnail FROM courses")
    courses = [{"title": row[0], "url": row[1], "thumbnail": row[2]} for row in cursor.fetchall()]
    conn.close()
    
    print(f"🔥 Returning {len(courses)} courses")  # Debug log
    return jsonify(courses)

if __name__ == '__main__':
    app.run(debug=True)
