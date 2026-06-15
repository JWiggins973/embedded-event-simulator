import sqlite3

# Initialize the database name
DB_NAME = 'events.db'

# Get a connection to the database
def get_connection():
    return sqlite3.connect(DB_NAME)

# Initialize the database
def init_database():
    conn = get_connection()

    with conn:
        cursor = conn.cursor()  
        cursor.execute("""CREATE TABLE IF NOT EXISTS Events (
                id INTEGER PRIMARY KEY, 
                event_type TEXT, 
                timestamp DATETIME,
                severity TEXT,
                duration INTEGER)      
                """)

# Insert a new event into the database
def insert_event(event_type, timestamp, severity, duration):
    conn = get_connection()
    with conn:
        conn.execute("INSERT INTO Events (event_type, timestamp, severity, duration) VALUES (?, ?, ?, ?)", (event_type, timestamp, severity, duration))
    
# Get specific events by type
def get_events_by_type(event_type):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE event_type = ?", (event_type,))
        return cursor.fetchall()

# Get all events from the database
def get_events():
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events")
        return cursor.fetchall()

# Get a summary of events by type
def get_summary():
    with get_connection() as conn:
        cursor = conn.execute("SELECT event_type, COUNT(*) FROM Events GROUP BY event_type")
        return cursor.fetchall()