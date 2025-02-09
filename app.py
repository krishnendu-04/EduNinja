from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

# Set up Flask app
app = Flask(__name__)

# Supabase configuration
url = "https://dkwojszgvuntyccquebc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrd29qc3pndnVudHljY3F1ZWJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNDY1ODQsImV4cCI6MjA1NDYyMjU4NH0.M7VKOCm0qYzBxX-I7busit5RB91gJV0PjRUzybNoZsI"
supabase: Client = create_client(url, key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_courses():
    query = request.args.get('query')
    if query:
        courses = fetch_courses_from_supabase(query)
        return jsonify(courses)
    else:
        return jsonify({"error": "No query provided"}), 400

def fetch_courses_from_supabase(query):
    # Fetch courses from Supabase table
    courses = supabase.table('courses').select('*').like('title', f"%{query}%").execute()
    return courses.data

if __name__ == '__main__':
    app.run(debug=True)
