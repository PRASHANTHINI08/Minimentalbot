"""
Configuration module for Mini Mental Health Tool.
Loads environment variables and defines bot settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Bot Settings ---
# Maximum number of message pairs (user + bot) to keep in history
MAX_HISTORY_LENGTH = 20

# Gemini model to use (free tier)
GEMINI_MODEL = "gemini-2.0-flash-lite"

# Generation parameters
GENERATION_CONFIG = {
    "temperature": 0.8,
    "max_output_tokens": 300,
    "top_p": 0.95,
    "top_k": 40,
}
