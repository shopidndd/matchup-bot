import sqlite3
from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.prompts import conversation_prompts
import time
from bot.services.user_service import search_users, get_active_users

# Example pairing logic
def pair_users(update: Update, context: CallbackContext):
    update.message.reply_text("Pairing users...")

def save_pairing(user1_id, user2_id):
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pairing_history (user1_id, user2_id)
        VALUES (?, ?)
    """, (user1_id, user2_id))
    conn.commit()
    conn.close()

def update_points(user_id, points):
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()


def networking_night():
    users = search_users({"preferences": "business"})
    pair_users(users)


def speed_dating():
    while True:
        users = get_active_users()
        pair_users(users)
        time.sleep(300)  # Wait 5 minutes before re-pairing

def preferences(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not context.args:
        update.message.reply_text("Usage: /preferences [general|business|love]")
        return
    preference = context.args[0].lower()
    if preference not in conversation_prompts:
        update.message.reply_text("Invalid preference. Please choose from general, business, or love.")
        return
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET preferences = ? WHERE user_id = ?", (preference, user_id))
    conn.commit()
    conn.close()
    update.message.reply_text(f"Your preference has been set to {preference}!")

# Pairing logic with preferences
def advanced_pairing(context: CallbackContext):
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()

    # Fetch active users
    cursor.execute("""
        SELECT user_id, preferences, last_active, region FROM users WHERE is_active = 1
    """)
    users = cursor.fetchall()
    conn.close()

    if len(users) < 2:
        return  # Not enough users

    # Sort users by activity and region
    users = sorted(users, key=lambda x: (x[2], x[3]), reverse=True)

    # Pair users with the same preferences
    paired = []
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            if users[i][1] == users[j][1] and users[i][3] == users[j][3]:
                paired.append((users[i][0], users[j][0]))
                save_pairing(users[i][0], users[j][0])
                break

    # Notify paired users
    bot = context.bot
    for user1, user2 in paired:
        bot.send_message(user1, "You've been paired!")
        bot.send_message(user2, "You've been paired!")

