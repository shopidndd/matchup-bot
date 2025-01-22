from telegram.ext import Updater, CommandHandler
from bot.handlers.command_handlers import start, preferences, feedback
from bot.utils.database import create_database
from bot.services.notification_service import set_bot_instance
from bot.handlers.message_handlers import register_message_handler
from bot.handlers.callback_handlers import register_callback_handlers
from bot.utils.config import BOT_TOKEN, DATABASE_FILE

from telegram.ext import Application, CommandHandler
from bot.handlers.command_handlers import start, preferences, feedback

async def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("preferences", preferences))
    application.add_handler(CommandHandler("feedback", feedback))

    # Run the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    # Set bot instance for services
