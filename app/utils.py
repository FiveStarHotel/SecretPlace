import secrets
from datetime import UTC, datetime


def generate_token(length = 20):
    return secrets.token_urlsafe()

def utc_now():
    return datetime.now(UTC).replace(tzinfo=None)

