import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger("neuroscan_contacts")

# Define path to SQLite database inside backend/data/
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "contacts.db")

def init_db():
    """Ensure database directory and contacts table exist."""
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT NOT NULL,
                    location TEXT NOT NULL,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info(f"Contacts database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize contacts database: {e}")

def create_contact(
    full_name: str,
    phone: str,
    location: str,
    email: Optional[str] = None,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """Insert a new contact submission into SQLite database."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO contacts (full_name, email, phone, location, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (full_name.strip(), (email or "").strip(), phone.strip(), location.strip(), (message or "").strip(), datetime.now().isoformat())
        )
        conn.commit()
        contact_id = cursor.lastrowid
        return {
            "id": contact_id,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "location": location,
            "message": message,
            "status": "received"
        }

def get_contacts(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve recent contact submissions."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
