import sqlite3
from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.prompts import conversation_prompts, premium_prompts
import random

# Example function
def search_users(update: Update, context: CallbackContext):
    update.message.reply_text("Searching for users...")

def get_prompt(is_premium):
    if is_premium:
        return random.choice(premium_prompts)
    return random.choice(conversation_prompts)


def add_user(user_id, username, preferences=""):
    """
    Adds or updates a user in the database.
    """
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, username, preferences)
        VALUES (?, ?, ?)
    """, (user_id, username, preferences))
    conn.commit()
    conn.close()

def search_users(filter_criteria):
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    
    # Build query dynamically based on filters
    query = "SELECT user_id FROM users WHERE is_active = 1"
    params = []
    for key, value in filter_criteria.items():
        query += f" AND {key} = ?"
        params.append(value)
    
    cursor.execute(query, params)
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def update_preferences(user_id, preferences):
    """
    Updates the preferences of a user.
    """
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET preferences = ?
        WHERE user_id = ?
    """, (preferences, user_id))
    conn.commit()
    conn.close()

# Function to retrieve all active users
def get_active_users():
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE is_active = 1")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def user_insights(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM pairing_history WHERE user1_id = ? OR user2_id = ?
    """, (user_id, user_id))
    connections = cursor.fetchone()[0]
    conn.close()

    update.message.reply_text(f"You have made {connections} connections!")

