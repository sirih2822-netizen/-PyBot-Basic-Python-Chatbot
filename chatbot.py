"""
chatbot.py - Core Rule-Based Chatbot Logic
CodeAlpha Python Programming Internship - Task 4: Basic Chatbot

Demonstrated Python Concepts:
1. Functions (normalize_text, match_intent, get_bot_response, run_cli)
2. If-Elif-Else statements (intent selection and validation routing)
3. Loops (iterating over pattern tuples, token inspection, and interactive CLI loop)
4. User input and output (validation, console input/output in CLI mode, HTTP integration)
"""

import string
from typing import List, Optional


def normalize_text(text: str) -> str:
    """
    Validates and normalizes user input text.

    Steps:
    1. Validate that input is a string instance.
    2. Strip leading and trailing whitespace.
    3. Ensure input is not empty or whitespace-only.
    4. Convert to lowercase for case-insensitive matching.
    5. Strip common outer punctuation while preserving interior words.

    Raises:
        TypeError: If input is not a string.
        ValueError: If input is empty or whitespace-only.
    """
    if not isinstance(text, str):
        raise TypeError("Message input must be a string.")

    trimmed = text.strip()
    if not trimmed:
        raise ValueError("Message cannot be empty.")

    # Convert to lowercase
    lowered = trimmed.lower()

    # Strip outer punctuation characters (e.g., 'hello?!' -> 'hello')
    outer_punctuation = string.punctuation + "¡¿“”‘’"
    normalized = lowered.strip(outer_punctuation).strip()

    # If all characters were punctuation (e.g. '???'), fallback to original trimmed lowercase
    return normalized if normalized else lowered


def _matches_any_pattern(normalized_text: str, tokens: List[str], patterns: List[str]) -> bool:
    """
    Helper function using a loop to check if any pattern matches the message.
    Avoids false positive substring matches by comparing either full phrases
    or discrete token boundaries.
    """
    for pattern in patterns:
        # Exact match or phrase match
        if normalized_text == pattern:
            return True

        # Check multi-word phrase containment
        if " " in pattern:
            if pattern in normalized_text:
                return True
        else:
            # Single word pattern: match against discrete word tokens to prevent
            # false positives (e.g., "shine" should not trigger "hi")
            if pattern in tokens:
                return True

    return False


def get_bot_response(message: str) -> str:
    """
    Determines the chatbot response based on rule-based intent matching.

    Core logic employs explicit if-elif-else decision structures
    to route the normalized message to predefined responses.

    Args:
        message (str): Raw message string from the user.

    Returns:
        str: Predefined chatbot response string.

    Raises:
        TypeError: If message is not a string.
        ValueError: If message is empty or whitespace-only.
    """
    # 1. Validation and Normalization
    normalized = normalize_text(message)
    tokens = normalized.split()

    # 2. Rule-based pattern definitions
    greeting_patterns = [
        "hi", "hello", "hey", "good morning", "good afternoon",
        "good evening", "greetings", "hiya"
    ]
    wellbeing_patterns = [
        "how are you", "how are you doing", "how do you do", "how r u",
        "how are you today"
    ]
    identity_patterns = [
        "who are you", "what is your name", "what's your name",
        "whats your name", "who r u", "what are you"
    ]
    capability_patterns = [
        "what can you do", "help", "what do you do", "capabilities",
        "commands", "what are your features"
    ]
    thanks_patterns = [
        "thanks", "thank you", "thx", "thank u", "many thanks", "appreciate it"
    ]
    goodbye_patterns = [
        "bye", "goodbye", "see you", "see ya", "cya", "bye bye",
        "farewell", "have a nice day"
    ]

    # 3. Predefined responses required by the assignment specification
    RESP_GREETING = "Hi! Nice to meet you. How can I help you?"
    RESP_WELLBEING = "I'm fine, thanks! How are you?"
    RESP_IDENTITY = "I'm PyBot, a simple rule-based chatbot built with Python."
    RESP_CAPABILITIES = (
        "I can respond to simple greetings, answer a few predefined questions, "
        "and demonstrate a basic Python chatbot."
    )
    RESP_THANKS = "You're welcome!"
    RESP_GOODBYE = "Goodbye! Have a great day!"
    RESP_UNKNOWN = (
        "Sorry, I don't understand that message yet. "
        "Try saying hello, asking how I am, or typing help."
    )

    # 4. Explicit if-elif-else decision tree
    # Order matters: check more specific phrases (wellbeing, identity, capabilities)
    # before general single-word greetings.
    if _matches_any_pattern(normalized, tokens, wellbeing_patterns):
        return RESP_WELLBEING
    elif _matches_any_pattern(normalized, tokens, identity_patterns):
        return RESP_IDENTITY
    elif _matches_any_pattern(normalized, tokens, capability_patterns):
        return RESP_CAPABILITIES
    elif _matches_any_pattern(normalized, tokens, thanks_patterns):
        return RESP_THANKS
    elif _matches_any_pattern(normalized, tokens, goodbye_patterns):
        return RESP_GOODBYE
    elif _matches_any_pattern(normalized, tokens, greeting_patterns):
        return RESP_GREETING
    else:
        return RESP_UNKNOWN


def run_cli() -> None:
    """
    Console CLI loop demonstrating terminal input/output and loop iteration.
    Allows running the chatbot standalone from the command prompt.
    """
    print("=" * 60)
    print(" PyBot — Basic Python Chatbot (Console Mode)")
    print(" CodeAlpha Python Programming Internship - Task 4")
    print(" Type 'bye', 'exit', or 'quit' to end the conversation.")
    print("=" * 60)
    print("PyBot: Hi! I'm PyBot, your basic Python chatbot. Say hello to get started.\n")

    while True:
        try:
            user_input = input("You: ")
            trimmed = user_input.strip()

            if not trimmed:
                print("PyBot: Please enter a non-empty message.\n")
                continue

            if trimmed.lower() in ["exit", "quit"]:
                print("PyBot: Goodbye! Have a great day!")
                break

            response = get_bot_response(user_input)
            print(f"PyBot: {response}\n")

            if trimmed.lower() in ["bye", "goodbye"]:
                print("(Session ended. Run again to chat more!)")
                break

        except (KeyboardInterrupt, EOFError):
            print("\nPyBot: Goodbye! Have a great day!")
            break


if __name__ == "__main__":
    run_cli()
