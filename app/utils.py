import secrets
from datetime import UTC, datetime


def generate_token(length = 32):
    return secrets.token_urlsafe()
