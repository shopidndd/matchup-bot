from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from telegram.ext import MessageHandler, Filters

# Function to register message handlers
def register_message_handler(dispatcher):
    """
    Registers message handlers to the dispatcher.
    """
    # Handle general text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))
    # Handle media files (photos and videos)
    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.video, handle_media_message))

def handle_text_message(update, context):
    """
    Handles text messages sent by users.
    """
    user_message = update.message.text
    update.message.reply_text(f"You said: {user_message}")

    update.message.reply_text(f"You said: {update.message.text}")
    if "hello" in user_message.lower():
        update.message.reply_text("Hi there! How can I assist you today?")
    elif "bye" in user_message.lower():
        update.message.reply_text("Goodbye! See you again soon.")
    else:
        update.message.reply_text("I’m not sure how to respond to that.")

def handle_media_message(update, context):
    """
    Handles media messages like photos and videos sent by users.
    """

    if update.message.photo:
        update.message.reply_text("Nice photo! 📸")
    elif update.message.video:
        update.message.reply_text("Thanks for sharing the video! 🎥")
    else:
        update.message.reply_text("I received something, but I’m not sure what it is.")


