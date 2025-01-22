from telegram.ext import CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Set bot globally
bot = None

print("Loading notification_service.py...")

def set_bot_instance(bot):
    global bot_instance
    bot_instance = bot

print("set_bot_instance is defined.")

def send_notification(user_id, message):
    """
    Sends a notification message to a specific user using the bot instance.
    """
    if bot_instance:
        bot_instance.send_message(chat_id=user_id, text=message)
    else:
        raise RuntimeError("Bot instance is not set. Call set_bot_instance first.")

