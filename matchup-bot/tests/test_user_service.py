import sqlite3
import pytest
from bot.services.user_service import add_user

@pytest.fixture
def setup_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            preferences TEXT
        )
    """)
    yield conn
    conn.close()

def test_add_user(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    add_user(1, "test_user", "love")
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (1,))
    user = cursor.fetchone()

    assert user[0] == 1
    assert user[1] == "test_user"
    assert user[2] == "love"
