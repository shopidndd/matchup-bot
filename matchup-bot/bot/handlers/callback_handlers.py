from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import sqlite3

# Example Service Import
from bot.services.pairing_service import pair_users


# Callback: Handle Button Clicks
def handle_callback(update: Update, context: CallbackContext):
    """
    Handles callback queries from inline buttons.
    """
    query = update.callback_query
    if query:
        query.answer("Callback received!")
        query.edit_message_text(text="You clicked a button!")


# Command: Leaderboard
def leaderboard(update: Update, context: CallbackContext):
    """
    Displays the top 10 users with the highest points.
    """
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10")
    leaders = cursor.fetchall()
    conn.close()

    if not leaders:
        update.message.reply_text("Leaderboard is currently empty.")
    else:
        leaderboard_text = "\n".join([f"{i+1}. {row[0]} - {row[1]} points" for i, row in enumerate(leaders)])
        update.message.reply_text(f"Leaderboard:\n{leaderboard_text}")


# Command: Report User
def report(update: Update, context: CallbackContext):
    """
    Allows users to report issues or other users.
    """
    if not context.args:
        update.message.reply_text("Usage: /report [reason]")
        return
    reason = " ".join(context.args)
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (user_id, reason) VALUES (?, ?)", (user_id, reason))
    conn.commit()
    conn.close()

    update.message.reply_text("Your report has been logged. Thank you!")


# Command: Schedule
def set_schedule(update: Update, context: CallbackContext):
    """
    Allows users to set their availability schedule.
    """
    if not context.args:
        update.message.reply_text("Usage: /schedule [time_slot]")
        return
    time_slot = context.args[0]
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET schedule = ? WHERE user_id = ?", (time_slot, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Your schedule has been set to {time_slot}!")


# Command: Set Custom Greeting
def set_greeting(update: Update, context: CallbackContext):
    """
    Allows users to set a custom greeting.
    """
    if not context.args:
        update.message.reply_text("Usage: /greeting [message]")
        return
    greeting = " ".join(context.args)
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET custom_greeting = ? WHERE user_id = ?", (greeting, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Your greeting has been set to: {greeting}")


# Command: Select Prompt Category
def select_prompt_category(update: Update, context: CallbackContext):
    """
    Allows users to select a conversation prompt category.
    """
    if not context.args:
        update.message.reply_text("Usage: /prompt_category [business|love|general]")
        return
    category = context.args[0].lower()
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET prompt_category = ? WHERE user_id = ?", (category, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Prompt category set to: {category}")


# Command: Rename Bot
def rename_bot(update: Update, context: CallbackContext):
    """
    Allows users to rename their bot.
    """
    if not context.args:
        update.message.reply_text("Usage: /rename_bot [name]")
        return
    bot_name = " ".join(context.args)
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET bot_name = ? WHERE user_id = ?", (bot_name, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Your bot is now named: {bot_name}")


# Command: Accessibility
def set_accessibility(update: Update, context: CallbackContext):
    """
    Allows users to set accessibility preferences.
    """
    if not context.args:
        update.message.reply_text("Usage: /accessibility [contrast|large_fonts]")
        return
    preference = context.args[0].lower()
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET accessibility = ? WHERE user_id = ?", (preference, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Accessibility preference set to {preference}.")


# Register Callback Handlers
def register_callback_handlers(dispatcher):
    """
    Registers callback handlers to the dispatcher.
    """
    dispatcher.add_handler(CommandHandler("leaderboard", leaderboard))
    dispatcher.add_handler(CommandHandler("report", report))
    dispatcher.add_handler(CommandHandler("schedule", set_schedule))
    dispatcher.add_handler(CommandHandler("greeting", set_greeting))
    dispatcher.add_handler(CommandHandler("prompt_category", select_prompt_category))
    dispatcher.add_handler(CommandHandler("rename_bot", rename_bot))
    dispatcher.add_handler(CommandHandler("accessibility", set_accessibility))
