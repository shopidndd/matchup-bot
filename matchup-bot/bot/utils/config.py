import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration values
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Retrieve bot token
DATABASE_FILE = os.getenv('DATABASE_FILE', 'enhanced_pairing_bot.db')  # Default database file
