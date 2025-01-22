import pytest
from unittest.mock import Mock, MagicMock
from telegram import Update, Message
from telegram.ext import CallbackContext
from bot.handlers.command_handlers import start, preferences, feedback

# Fixtures for mocked Update and Context
@pytest.fixture
def mock_update():
    """Fixture to create a mocked Telegram Update object."""
    update = Mock(spec=Update)
    update.message = Mock(spec=Message)
    return update

@pytest.fixture
def mock_context():
    """Fixture to create a mocked CallbackContext object."""
    return Mock(spec=CallbackContext)

# Test for /start command
def test_start_command(mock_update, mock_context):
    """Test the /start command handler."""
    mock_update.message.reply_text = MagicMock()

    start(mock_update, mock_context)

    # Assert that the correct reply was sent
    mock_update.message.reply_text.assert_called_once_with("Welcome to the Enhanced Pairing Bot!")

# Test for /preferences command
def test_preferences_command(mock_update, mock_context):
    """Test the /preferences command handler."""
    mock_update.message.reply_text = MagicMock()

    preferences(mock_update, mock_context)

    # Assert that the correct reply was sent
    mock_update.message.reply_text.assert_called_once_with("Set your preferences using the command.")

# Test for /feedback command
def test_feedback_command(mock_update, mock_context):
    """Test the /feedback command handler."""
    mock_update.message.reply_text = MagicMock()

    feedback(mock_update, mock_context)

    # Assert that the correct reply was sent
    mock_update.message.reply_text.assert_called_once_with("Thank you for your feedback!")
