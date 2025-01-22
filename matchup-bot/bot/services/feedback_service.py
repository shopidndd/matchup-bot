import sqlite3
from telegram import Update
from telegram.ext import CallbackContext
from langdetect import detect  # Language detection library
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Example function
def process_feedback(update: Update, context: CallbackContext):
    language = detect(update.message.text)
    update.message.reply_text(f"Detected language: {language}")

def save_feedback(user_id, feedback):
    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (user_id, feedback)
        VALUES (?, ?)
    """, (user_id, feedback))
    conn.commit()
    conn.close()

def sync_with_calendar(event_title, start_time, end_time):
    creds = Credentials.from_authorized_user_file('credentials.json')
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': event_title,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'}
    }
    service.events().insert(calendarId='primary', body=event).execute()

def feedback(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    feedback_text = " ".join(context.args)
    if feedback_text:
        save_feedback(user_id, feedback_text)
        update.message.reply_text("Thank you for your feedback!")
    else:
        update.message.reply_text("Please provide your feedback after the command, e.g., /feedback It was great!")

def detect_language(update: Update, context: CallbackContext):
    user_text = update.message.text
    user_lang = detect(user_text)
    update.message.reply_text(f"Detected language: {user_lang}")

# Set preferred language
def set_language(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /language [language_code]")
        return
    language_code = context.args[0]
    user_id = update.effective_user.id

    conn = sqlite3.connect("enhanced_pairing_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language_code, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Language set to {language_code}!")

# Example function using RandomForestClassifier
def analyze_data(update: Update, context: CallbackContext):
    data = pd.DataFrame({
        'Feature1': [1, 2, 3],
        'Feature2': [4, 5, 6],
        'Label': [0, 1, 0]
    })
    X = data[['Feature1', 'Feature2']]
    y = data['Label']
    model = RandomForestClassifier()
    model.fit(X, y)
    update.message.reply_text("Model trained successfully!")


# Training data: [user1_features, user2_features, match_success]
data = pd.read_csv("pairing_data.csv")
X = data.drop(columns=["match_success"])
y = data["match_success"]

# Train a model
model = RandomForestClassifier()
model.fit(X, y)

def predict_match(user1_features, user2_features):
    combined_features = user1_features + user2_features
    prediction = model.predict([combined_features])
    return prediction[0]  # 1 for successful match, 0 otherwise

