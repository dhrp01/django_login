import re
from re import Match

def is_valid_email(email: str) -> Match[str] | None:
    """Check that the email is format *@.*"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone: str) -> Match[str] | None:
    """Check that given phone number is valid, all characters in strings are numbers"""
    return re.match(r"^\+?1?\d{9,15}$", phone)

def is_invalid_password(password: str) -> list:
    """Check if the password is invalid (Strength of the password)
    1. Is 8 characters long
    2. Has upper case charaters
    3. Has lower case characters
    4. Has special characters
    5. Has number characters

    Returns:
        A list containing the error messages in case the password is not valid otherwise an empty list if password is valid.
    """
    messages = []
    if len(password) < 8:
        messages.append({"message":"Password must be 8 characters long.", "status": "error"})
    elif not re.search(r'[A-Z]', password):
        messages.append({"message":"Password must include upper case characters.", "status": "error"})
    elif not re.search(r'[a-z]', password):
        messages.append({"message":"Password must include lower case characters.", "status": "error"})
    elif not re.search(r'[\W_]', password):
        messages.append({"message":"Password must include special characters.", "status": "error"})
    elif not re.search(r'[0-9]', password):
        messages.append({"message":"Password must include digits.", "status": "error"})
    return messages
