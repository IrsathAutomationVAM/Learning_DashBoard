from Agents.database import get_connection

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_date TEXT,
        accomplishments TEXT,
        learnings TEXT,
        blockers TEXT,
        plan TEXT,
        productivity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_tracker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learning_date TEXT,
        category TEXT,
        notes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certification_name TEXT,
        progress INTEGER,
        target_date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
