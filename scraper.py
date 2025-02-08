import requests
import logging
import isodate

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# YouTube API Key (Replace with your actual key)
YOUTUBE_API_KEY = "AIzaSyB1xQTaELG_XQ5BbZjwVx1y_-4M1uzmlP0"

def fetch_youtube_courses(query, max_results=5):
    """
    Fetches YouTube courses based on a given query.
    Retrieves video title, URL, thumbnail, views, duration, likes, comments, channel name, and upload date.
    """
    logging.info(f"📡 Fetching courses for '{query}' from YouTube API...")

    # YouTube Search API URL
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={max_results}&q={query}%20full%20course&key={YOUTUBE_API_KEY}"
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        logging.error(f"❌ API Error {search_response.status_code}: {search_response.text}")
        return []

    search_data = search_response.json()
    
    # Extract video IDs
    video_ids = [item["id"]["videoId"] for item in search_data.get("items", []) if "videoId" in item["id"]]
    if not video_ids:
        logging.warning("⚠️ No videos found.")
        return []

    video_ids_str = ",".join(video_ids)

    # YouTube Video Details API URL
    details_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails,snippet&id={video_ids_str}&key={YOUTUBE_API_KEY}"
    details_response = requests.get(details_url)

    if details_response.status_code != 200:
        logging.error(f"❌ API Error {details_response.status_code}: {details_response.text}")
        return []

    details_data = details_response.json()
    
    courses = []
    for item in details_data.get("items", []):
        video_id = item["id"]
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        content_details = item.get("contentDetails", {})

        title = snippet["title"]
        thumbnail = snippet["thumbnails"]["high"]["url"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        channel = snippet["channelTitle"]
        upload_date = snippet["publishedAt"].split("T")[0]  # Extract only the date

        views = stats.get("viewCount", "0")
        likes = stats.get("likeCount", "0")
        comments = stats.get("commentCount", "0")

        # Convert YouTube's ISO 8601 duration to readable format
        duration_iso = content_details.get("duration", "N/A")
        try:
            duration = str(isodate.parse_duration(duration_iso))
        except:
            duration = "Unknown"

        courses.append({
            "title": title,
            "url": url,
            "thumbnail": thumbnail,
            "views": views,
            "likes": likes,
            "comments": comments,
            "duration": duration,
            "channel": channel,
            "upload_date": upload_date
        })

    logging.info(f"✅ Fetched {len(courses)} courses successfully!")
    return courses

# Example Usage
if __name__ == "__main__":
    query = input("Enter a topic to search for courses: ")
    courses = fetch_youtube_courses(query)

    for idx, course in enumerate(courses, 1):
        print(f"\n📚 Course {idx}: {course['title']}")
        print(f"🔗 URL: {course['url']}")
        print(f"👤 Channel: {course['channel']}")
        print(f"📅 Upload Date: {course['upload_date']}")
        print(f"⏳ Duration: {course['duration']}")
        print(f"👀 Views: {course['views']} | 👍 Likes: {course['likes']} | 💬 Comments: {course['comments']}")
