import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_FILE = 'enhanced_pairing_bot.db'
