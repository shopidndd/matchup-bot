import pytest
from telegram.ext import Updater, CommandHandler
from bot.main import main  # Assuming main.py initializes your bot

@pytest.fixture
def test_updater():
    """Create a mock updater instance."""
    return Updater(token="TEST_TOKEN", use_context=True)

def test_bot_initialization(updater):
    """Test bot initialization."""
    dispatcher = updater.dispatcher

    # Check if dispatcher is initialized
    assert dispatcher is not None

    # Example: Add a dummy handler to ensure handlers can be registered
    def dummy_handler(update, context):
        pass

    handler = CommandHandler("dummy", dummy_handler)
    dispatcher.add_handler(handler)

    # Check if handler is added
    assert handler in dispatcher.handlers[0]
