# YouTube News Channel Analysis

Automated data collection and analysis of top comments from major news channels (BBC, NBC, Fox News).

## Overview

This project collects video metadata and top comments from YouTube news channels twice daily, storing the data for trend analysis and engagement pattern detection.

## Features

- ✅ Automated data collection via GitHub Actions (9 AM & 9 PM daily)
- ✅ Tracks video views over time
- ✅ Collects top 3 comments per video
- ✅ SQLite database with relational structure
- 🚧 Analysis dashboard (coming soon)

## Tech Stack

- **Data Collection**: YouTube Data API v3, Python
- **Storage**: SQLite
- **Automation**: GitHub Actions (CI/CD)
- **Analysis**: Jupyter, Pandas (coming soon)

## Project Structure
youtube-comment-analysis/
├── data/
│   └── youtube_data.db          # SQLite database
├── data_collection/
│   ├── collect.py               # Main collection script
│   ├── youtube_api.py           # YouTube API wrapper
│   └── database.py              # Database operations
├── .github/
│   └── workflows/
│       └── collect_data.yml     # Automated collection schedule
└── requirements.txt

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with your YouTube API key
6. Run manually: `python data_collection/collect.py`

## Automation

Data collection runs automatically via GitHub Actions twice daily. See workflow configuration in `.github/workflows/collect_data.yml`.

## Database Schema

**videos** - Video metadata
- video_id (PK)
- channel_id
- title
- description
- publish_date

**video_views** - View count snapshots
- snapshot_id (PK)
- video_id (FK)
- collected_at
- view_count

**comments** - Top 3 comments per video
- comment_id (PK)
- video_id (FK)
- author_name
- comment_text
- like_count
- published_at
- collected_at

## Future Enhancements

- [ ] Sentiment analysis on comments
- [ ] Interactive Streamlit dashboard
- [ ] Channel comparison metrics
- [ ] Engagement trend visualization

## License

MIT