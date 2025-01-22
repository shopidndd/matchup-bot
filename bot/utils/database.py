import sqlite3

def create_database():
    """
    Creates the database and initializes all required tables for the bot.
    """
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            preferences TEXT DEFAULT NULL,
            points INTEGER DEFAULT 0,
            schedule TEXT DEFAULT NULL,
            custom_greeting TEXT DEFAULT NULL,
            prompt_category TEXT DEFAULT NULL,
            bot_name TEXT DEFAULT 'Bot',
            accessibility TEXT DEFAULT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)

    # Pairing History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pairing_history (
            pair_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER,
            user2_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users(user_id),
            FOREIGN KEY (user2_id) REFERENCES users(user_id)
        )
    """)

    # Feedback Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Notifications Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            scheduled_time DATETIME,
            sent INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Prompts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,  -- E.g., 'business', 'love', 'general'
            text TEXT,
            is_premium INTEGER DEFAULT 0
        )
    """)

    # Events Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_type TEXT,  -- E.g., 'networking', 'speed_dating'
            event_time DATETIME,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(user_id)
        )
    """)

    # Event Participants Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_participants (
            event_id INTEGER,
            user_id INTEGER,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (event_id, user_id),
            FOREIGN KEY (event_id) REFERENCES events(event_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Premium Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS premium_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database created successfully.")


# Call the function to create the database
if __name__ == "__main__":
    create_database()
