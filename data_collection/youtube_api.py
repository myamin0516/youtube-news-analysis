from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Description filtering rules
FILTERS = {
    "UC16niRr50-MSBwiO3YDb3RA": "Subscribe here:",   # BBC
    "UCeY0bbntWzzVIaj2z3QigXg": "For more context",  # NBC
    "UCXIJgqnII2ZOINSWNOGFThA": "Become a Channel"   # Fox
}

def clean_description(channel_id, description):
    marker = FILTERS.get(channel_id, None)
    if marker and marker in description:
        return description.split(marker)[0].strip()
    return description.strip()

def fetch_recent_videos(channel_id, since, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    published_after_str = since.replace(microsecond=0).isoformat().split('+')[0] + 'Z'
    
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        publishedAfter=published_after_str,
        type="video",
        order="date",
        maxResults=20
    )
    search_response = request.execute()
    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    
    if not video_ids:
        return []
    
    details = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()
    
    videos = []
    for item in details.get("items", []):
        snippet = item["snippet"]
        stats = item["statistics"]
        videos.append({
            "id": item["id"],
            "channelId": snippet["channelId"],
            "title": snippet["title"],
            "description": clean_description(snippet["channelId"], snippet.get("description", "")),
            "publishedAt": snippet["publishedAt"],
            "viewCount": int(stats.get("viewCount", 0))
        })
    
    return videos

def fetch_top_comments(video_id, api_key, max_comments=3):
    """
    Fetch the top N comments for a given video based on relevance/likes.
    Returns a list of comment dictionaries.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="relevance",  # Top comments by relevance
            maxResults=max_comments,
            textFormat="plainText"
        )
        response = request.execute()
        
        comments = []
        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "id": item["snippet"]["topLevelComment"]["id"],
                "authorName": top_comment["authorDisplayName"],
                "text": top_comment["textDisplay"],
                "likeCount": top_comment["likeCount"],
                "publishedAt": top_comment["publishedAt"]
            })
        
        return comments
    
    except Exception as e:
        # Comments may be disabled or unavailable
        print(f"  ⚠ Could not fetch comments: {str(e)}")
        return []