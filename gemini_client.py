"""
Gemini API client for generating emotionally supportive responses.
Uses the google-genai SDK with retry logic for rate limits.
"""

import time
import logging

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, GENERATION_CONFIG
from system_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Module-level client
_client = None


def initialize_gemini():
    """Configure the Gemini API client with the API key."""
    global _client

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please add it to your .env file."
        )

    _client = genai.Client(api_key=GEMINI_API_KEY)


def format_chat_history(chat_history: list) -> str:
    """
    Format the chat history into a readable string for the AI.

    Args:
        chat_history: List of dicts with 'role' and 'content' keys.

    Returns:
        Formatted string of the conversation history.
    """
    if not chat_history:
        return "No previous conversation."

    formatted = []
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "You"
        formatted.append(f"{role}: {msg['content']}")

    return "\n".join(formatted)


def generate_response(user_message: str, chat_history: list) -> str:
    """
    Generate an emotionally supportive response using Gemini.
    Includes retry logic for transient network and rate limit errors.

    Args:
        user_message: The current message from the user.
        chat_history: List of previous messages for context.

    Returns:
        The AI-generated response text.
    """
    global _client

    # Format the history for context
    history_text = format_chat_history(chat_history)

    # Build the full prompt
    prompt = (
        f"CHAT_HISTORY:\n{history_text}\n\n"
        f"USER_MESSAGE: {user_message}"
    )

    # Retry up to 3 times for transient errors
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Gemini API call attempt {attempt}/{max_retries}")

            # Generate response using the new SDK
            response = _client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=GENERATION_CONFIG["temperature"],
                    max_output_tokens=GENERATION_CONFIG["max_output_tokens"],
                    top_p=GENERATION_CONFIG["top_p"],
                    top_k=GENERATION_CONFIG["top_k"],
                ),
            )

            # Extract and return the text
            if response and response.text:
                logger.info("Gemini API response received successfully.")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response.")
                return (
                    "I'm here with you... sometimes words are hard to find. "
                    "Take your time, I'm listening."
                )

        except Exception as e:
            error_str = str(e)
            logger.error(f"[Gemini Error] Attempt {attempt}/{max_retries}: {e}")

            # Check if it's a rate limit error - wait longer
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries:
                    wait_time = 30
                    logger.info(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error("All retry attempts failed (rate limited).")
                    return (
                        "I'm taking a short breather right now... "
                        "give me a minute and try again. I'm not going anywhere."
                    )
            elif attempt < max_retries:
                logger.info("Retrying in 3 seconds...")
                time.sleep(3)
            else:
                logger.error("All retry attempts failed.")
                return (
                    "I'm sorry, I had a small hiccup on my end... "
                    "but I'm still here. Could you say that again?"
                )
