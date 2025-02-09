

import os
import logging
from supabase import create_client, Client
from googleapiclient.discovery import build

# Set up logging
logging.basicConfig(level=logging.INFO)

# Supabase configuration
url = "https://dkwojszgvuntyccquebc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrd29qc3pndnVudHljY3F1ZWJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNDY1ODQsImV4cCI6MjA1NDYyMjU4NH0.M7VKOCm0qYzBxX-I7busit5RB91gJV0PjRUzybNoZsI"
supabase: Client = create_client(url, key)

# Initialize YouTube API
API_KEY = 'AIzaSyB1xQTaELG_XQ5BbZjwVx1y_-4M1uzmlP0'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_youtube_courses(query):
    logging.info(f"📡 Fetching courses for '{query}' from YouTube API...")
    
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=5
    )
    
    response = request.execute()
    
    # Prepare data to store in Supabase
    for item in response['items']:
        video_id = item['id']['videoId']
        course_data = {
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "published_at": item['snippet']['publishedAt'],
            "thumbnail": item['snippet']['thumbnails']['high']['url']
        }

        # Insert into Supabase table 'courses'
        response = supabase.table('courses').insert(course_data).execute()
        print(response.status_code, response.json())
        logging.info(f"Added course: {item['snippet']['title']}")

# User input
query = input("Enter a topic to search for courses: ")
fetch_youtube_courses(query)

