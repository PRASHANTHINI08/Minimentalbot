import os
import google.generativeai as genai
from system_prompt import SYSTEM_PROMPT


def configure_gemini():
    """
    Configure the Gemini API with the API key from environment variables.
    Call this once at startup before making any API requests.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the .env file.")
    genai.configure(api_key=api_key)


def get_model():
    """
    Create and return a Gemini GenerativeModel instance
    with the system prompt baked in.
    """
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=SYSTEM_PROMPT,
    )
    return model


async def get_gemini_response(conversation_history: list[dict]) -> str:
    """
    Send the full conversation history to Gemini and return the reply.

    Args:
        conversation_history: A list of dicts with 'role' and 'parts' keys.
            - role: 'user' for user messages, 'model' for bot responses
            - parts: the text content of the message

    Returns:
        The AI-generated response text.

    Raises:
        Exception: If the Gemini API call fails for any reason.
    """
    model = get_model()

    # Start a chat session with the existing conversation history
    # (all messages except the latest one, which we'll send separately)
    history = conversation_history[:-1]  # everything except the last message
    latest_message = conversation_history[-1]["parts"]  # the newest user message

    chat = model.start_chat(history=history)

    # Send the latest message and get the response
    response = await chat.send_message_async(latest_message)

    return response.text
