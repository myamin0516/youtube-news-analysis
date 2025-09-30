import sqlite3
from datetime import datetime

def init_db(conn):
    cur = conn.cursor()
    
    # Videos table - core metadata
    cur.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            channel_id TEXT,
            title TEXT,
            description TEXT,
            publish_date TEXT
        )
    """)
    
    # Video views snapshots - track views over time
    cur.execute("""
        CREATE TABLE IF NOT EXISTS video_views (
            snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            collected_at TEXT,
            view_count INTEGER,
            FOREIGN KEY(video_id) REFERENCES videos(video_id)
        )
    """)
    
    # Comments table - stores top comments for each video
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id TEXT PRIMARY KEY,
            video_id TEXT,
            author_name TEXT,
            comment_text TEXT,
            like_count INTEGER,
            published_at TEXT,
            collected_at TEXT,
            FOREIGN KEY(video_id) REFERENCES videos(video_id)
        )
    """)
    
    # Create indexes for better query performance
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_views_video 
        ON video_views(video_id)
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_comments_video 
        ON comments(video_id)
    """)
    
    conn.commit()

def insert_video(conn, video):
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO videos (video_id, channel_id, title, description, publish_date)
        VALUES (?, ?, ?, ?, ?)
    """, (video["id"], video["channelId"], video["title"], video["description"], video["publishedAt"]))
    return video["id"]

def insert_snapshot(conn, video_id, view_count):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO video_views (video_id, collected_at, view_count)
        VALUES (?, ?, ?)
    """, (video_id, datetime.utcnow().isoformat(), view_count))

def insert_comments(conn, video_id, comments):
    cur = conn.cursor()
    collected_at = datetime.utcnow().isoformat()
    
    for comment in comments:
        cur.execute("""
            INSERT OR IGNORE INTO comments 
            (comment_id, video_id, author_name, comment_text, like_count, published_at, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            comment["id"],
            video_id,
            comment["authorName"],
            comment["text"],
            comment["likeCount"],
            comment["publishedAt"],
            collected_at
        ))