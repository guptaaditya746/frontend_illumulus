# db/story_logger.py

import sqlite3
import json
import os
from datetime import datetime

# Place the DB alongside feedback.db
DB_PATH = os.path.join(os.path.dirname(__file__), "stories.db")

def init_db():
    """Create the stories table if it doesn’t already exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_profile TEXT NOT NULL,
            seed TEXT NOT NULL,
            paragraphs TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_story(user_profile: dict, seed: dict, paragraphs: list):
    """
    Persist one full story run.
    
    Args:
      user_profile: dict of age, gender, emotion, objects, etc.
      seed: dict with keys "prompt", "genre", "elements"
      paragraphs: list of story strings in order
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO stories (timestamp, user_profile, seed, paragraphs)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        json.dumps(user_profile),
        json.dumps(seed),
        json.dumps(paragraphs)
    ))
    conn.commit()
    conn.close()

def fetch_all_stories():
    """Return a list of all logged stories as Python dicts."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, user_profile, seed, paragraphs FROM stories")
    rows = c.fetchall()
    conn.close()

    results = []
    for id_, ts, up_json, seed_json, paras_json in rows:
        results.append({
            "id": id_,
            "timestamp": ts,
            "user_profile": json.loads(up_json),
            "seed": json.loads(seed_json),
            "paragraphs": json.loads(paras_json)
        })
    return results
