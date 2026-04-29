"""
Mini Mental Health Tool -- Telegram Chatbot
A soft, emotionally supportive companion for college students.

Main entry point: initializes the bot and starts polling for messages.
"""

import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN
from gemini import configure_gemini
from handlers import start_command, help_command, reset_command, handle_message


# --- Logging Setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and run the Telegram bot."""

    # Validate token
    if not TELEGRAM_BOT_TOKEN:
        print("=" * 50)
        print("ERROR: TELEGRAM_BOT_TOKEN is not set!")
        print("Please create a .env file with your bot token.")
        print("See .env.example for the format.")
        print("=" * 50)
        return

    # Initialize Gemini API
    try:
        configure_gemini()
        logger.info("[OK] Gemini API initialized successfully.")
    except ValueError as e:
        print(f"ERROR: {e}")
        return

    # Build the Telegram bot application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))

    # Register message handler (handles all non-command text messages)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("=" * 50)
    print("Mini Mental Health Tool is running!")
    print("   Send /start to your bot on Telegram.")
    print("   Press Ctrl+C to stop.")
    print("=" * 50)

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
