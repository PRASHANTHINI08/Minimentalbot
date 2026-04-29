"""
Telegram bot handlers for commands and messages.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_HISTORY_LENGTH
from gemini import get_gemini_response
from safety import check_safety, get_safety_resources


# --- Welcome & Disclaimer ---
WELCOME_MESSAGE = (
    "Hey there 🤍\n\n"
    "I'm your Mini Mental Health companion — "
    "a safe little space for you to share what's on your mind.\n\n"
    "You can rant, vent, or just talk. I'm here to listen.\n\n"
    "Just type whatever you're feeling, and I'll be right here.\n\n"
    "—\n"
    "⚠️ Disclaimer: I'm not a therapist or a doctor. "
    "I'm here to listen and support, but please reach out to "
    "a real person or a helpline if you're going through something serious.\n\n"
    "Type /help to see what I can do."
)

HELP_MESSAGE = (
    "Here's how you can use me:\n\n"
    "💬 Just type anything — I'll listen and respond.\n"
    "🔄 /reset — Clear our conversation and start fresh.\n"
    "❓ /help — See this message again.\n\n"
    "You can talk in English or Tanglish — I'll match your style.\n\n"
    "I'm here for you 🤍"
)

RESET_MESSAGE = (
    "Our conversation has been reset. "
    "Fresh start — whenever you're ready to talk, I'm here 🤍"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command — greet the user and initialize history."""
    # Initialize empty chat history
    context.user_data["chat_history"] = []

    await update.message.reply_text(WELCOME_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command — show usage instructions."""
    await update.message.reply_text(HELP_MESSAGE)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /reset command — clear conversation history."""
    context.user_data["chat_history"] = []

    await update.message.reply_text(RESET_MESSAGE)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle all incoming text messages.
    This is the core conversation loop.
    """
    user_message = update.message.text

    # Skip empty messages
    if not user_message or not user_message.strip():
        return

    # Initialize history if not present (in case user didn't /start)
    if "chat_history" not in context.user_data:
        context.user_data["chat_history"] = []

    chat_history = context.user_data["chat_history"]

    # Append user message first (like Therapy repo does)
    chat_history.append({"role": "user", "parts": user_message})

    # Send typing indicator while generating response
    await update.message.chat.send_action("typing")

    try:
        # Generate AI response
        bot_response = await get_gemini_response(chat_history)

        # Check for crisis keywords and append safety resources
        if check_safety(user_message):
            bot_response += get_safety_resources()

        # Update chat history with model response
        chat_history.append({"role": "model", "parts": bot_response})
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Gemini API error: {e}")
        if chat_history:
            chat_history.pop()
        bot_response = "I'm having a little trouble right now, please try again in a moment 💙"

    # Trim history to keep only the last N message pairs
    if len(chat_history) > MAX_HISTORY_LENGTH * 2:
        context.user_data["chat_history"] = chat_history[-(MAX_HISTORY_LENGTH * 2):]

    # Send the response
    await update.message.reply_text(bot_response)
