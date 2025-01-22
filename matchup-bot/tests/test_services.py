import pytest
from bot.services.notification_service import send_notification
from bot.utils.database import setup_database, get_active_users

@pytest.fixture
def mock_context():
    """Mock a callback context with a bot instance."""
    class MockBot:
        def send_message(self, chat_id, text):
            self.chat_id = chat_id
            self.text = text

    class MockContext:
        def __init__(self):
            self.bot = MockBot()

    return MockContext()

def test_send_notification(mock_context):
    """Test sending a notification."""
    send_notification(user_id=123, message="Test Message", context=mock_context)
    assert mock_context.bot.chat_id == 123
    assert mock_context.bot.text == "Test Message"

def test_setup_database():
    """Test database setup."""
    setup_database()
    # Ensure the database file and tables are created
    import sqlite3
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    assert "users" in tables
    assert "pairing_history" in tables
    assert "feedback" in tables

def test_get_active_users():
    """Test fetching active users."""
    setup_database()  # Ensure tables are created
    import sqlite3
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username, is_active) VALUES (1, 'test_user', 1)")
    conn.commit()
    conn.close()

    active_users = get_active_users()
    assert active_users == [1]
