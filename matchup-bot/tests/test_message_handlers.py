import pytest
from unittest.mock import Mock, MagicMock
from telegram import Update, Message
from telegram.ext import CallbackContext
from bot.handlers.message_handlers import handle_text_message, handle_media_message

@pytest.fixture
def mock_update():
    """Create a mocked Telegram Update object."""
    update = Mock(spec=Update)
    update.message = Mock(spec=Message)
    return update

@pytest.fixture
def mock_context():
    """Create a mocked CallbackContext object."""
    return Mock(spec=CallbackContext)

def test_handle_text_message(mock_update, mock_context):
    mock_update.message.text = "Hello!"
    mock_update.message.reply_text = MagicMock()

    handle_text_message(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with("You said: Hello!")

def test_handle_media_message_photo(mock_update, mock_context):
    mock_update.message.photo = ["photo"]
    mock_update.message.reply_text = MagicMock()

    handle_media_message(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with("Nice photo! 📸")

def test_handle_media_message_video(mock_update, mock_context):
    mock_update.message.video = ["video"]
    mock_update.message.reply_text = MagicMock()

    handle_media_message(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with("Great video! 🎥")
