import os
import sqlite3
from datetime import datetime, timedelta, UTC
from youtube_api import fetch_recent_videos, fetch_top_comments
from database import init_db, insert_video, insert_snapshot, insert_comments
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
print(f"YouTube API Key loaded: {bool(YOUTUBE_API_KEY)}")

# Hardcoded channel IDs
CHANNELS = {
    "BBC News": "UC16niRr50-MSBwiO3YDb3RA",
    "NBC News": "UCeY0bbntWzzVIaj2z3QigXg",
    "Fox News": "UCXIJgqnII2ZOINSWNOGFThA"
}

def main():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/youtube_data.db")
    init_db(conn)
    
    # Get videos uploaded in last 48h
    since = datetime.now(UTC) - timedelta(hours=48)
    
    all_videos = []
    
    for channel_name, channel_id in CHANNELS.items():
        videos = fetch_recent_videos(channel_id, since, YOUTUBE_API_KEY)
        print(f"Fetched {len(videos)} videos for {channel_name}")
        all_videos.extend(videos)
    
    # Process each video
    for video in all_videos:
        video_id = insert_video(conn, video)  # Insert metadata (ignore duplicates)
        insert_snapshot(conn, video_id, video["viewCount"])  # Insert snapshot
        
        # Fetch top 3 comments
        print(f"Fetching comments for video: {video['title'][:50]}...")
        comments = fetch_top_comments(video_id, YOUTUBE_API_KEY, max_comments=3)
        
        if comments:
            insert_comments(conn, video_id, comments)
            print(f"  → Stored {len(comments)} comments")
        else:
            print(f"  → No comments available (may be disabled)")
    
    conn.commit()
    conn.close()
    print("✅ Run complete.")

if __name__ == "__main__":
    main()