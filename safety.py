"""
Safety module for crisis keyword detection.
Acts as a secondary safety net alongside the AI's system prompt.
"""

# Crisis-related phrases to watch for
CRISIS_KEYWORDS = [
    "give up",
    "can't continue",
    "cannot continue",
    "want to disappear",
    "no point living",
    "no point in living",
    "kill myself",
    "end my life",
    "want to die",
    "don't want to live",
    "dont want to live",
    "suicide",
    "self harm",
    "self-harm",
    "cut myself",
    "hurt myself",
    "better off dead",
    "no reason to live",
    "can't go on",
    "cant go on",
    "worthless",
    "ending it all",
    "end it all",
]


def check_safety(message: str) -> bool:
    """
    Check if a message contains crisis-related keywords.

    Args:
        message: The user's message text.

    Returns:
        True if crisis keywords are detected, False otherwise.
    """
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)


def get_safety_resources() -> str:
    """
    Return a gentle message with mental health helpline numbers.
    These are appended to the bot's response when crisis keywords are detected.
    """
    return (
        "\n\n---\n"
        "💛 You matter, and help is always available.\n\n"
        "If you need to talk to someone right now:\n"
        "• iCall – 9152987821\n"
        "• Vandrevala Foundation – 1860 2662 345 (24/7)\n"
        "• AASRA – 9820466726\n"
        "• Snehi – 044-24640050\n\n"
        "These are free, confidential, and available for you. 🤍"
    )
