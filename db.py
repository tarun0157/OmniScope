
import sqlite3
import json

DB_NAME = "omniscope.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Store individual agent reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            report TEXT NOT NULL,
            sources TEXT,
            status TEXT DEFAULT 'success'
        )
    """)

    # Store final coordinator briefings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS briefings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            briefing TEXT NOT NULL
        )
    """)

    # Track every research run
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status TEXT,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("OmniScope database initialized successfully!")


def save_report(domain, report, sources, status="success"):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reports (domain, report, sources, status)
        VALUES (?, ?, ?, ?)
    """, (domain, report, json.dumps(sources), status))

    connection.commit()
    connection.close()


def get_latest_reports():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT domain, report, sources, status, created_at
        FROM reports
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "domain": row[0],
            "report": row[1],
            "sources": json.loads(row[2]) if row[2] else [],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]


def save_briefing(briefing):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO briefings (briefing) VALUES (?)",
        (briefing,)
    )

    connection.commit()
    connection.close()


def get_latest_briefing():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT briefing, created_at
        FROM briefings
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "briefing": row[0],
            "created_at": row[1]
        }

    return None
