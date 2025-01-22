from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from bot.services.user_service import add_user, update_preferences

def start(update: Update, context: CallbackContext):
    """
    Handles the /start command.
    """
    update.message.reply_text("Welcome to the Enhanced Pairing Bot!")


# Command: /help
def help_command(update: Update, context: CallbackContext):
    """
    Provides a list of available commands.
    """
    help_text = (
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/preferences [options] - Set your preferences (e.g., /preferences love)\n"
        "/feedback [message] - Send feedback to the bot\n"
    )
    update.message.reply_text(help_text)


# Command: /preferences
def preferences(update: Update, context: CallbackContext):
    """
    Sets user preferences based on arguments provided.
    """
    user_id = update.effective_user.id

    if not context.args:
        update.message.reply_text("Usage: /preferences [option]\nOptions: love, business, hobbies")
        return

    preference = " ".join(context.args).lower()
    update_preferences(user_id, preference)
    update.message.reply_text(f"Your preferences have been updated to: {preference}")


# Command: /feedback
def feedback(update: Update, context: CallbackContext):
    """
    Handles user feedback.
    """
    if not context.args:
        update.message.reply_text("Please provide feedback after the command, e.g., /feedback Great bot!")
        return

    user_feedback = " ".join(context.args)
    update.message.reply_text(f"Thanks for your feedback: {user_feedback}")
    # You can add logic to save the feedback to a database.


# Register Command Handlers
def register_handlers(dispatcher):
    """
    Registers all command handlers to the dispatcher.
    """
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("preferences", preferences))
    dispatcher.add_handler(CommandHandler("feedback", feedback))
