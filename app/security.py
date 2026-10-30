import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy-password")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_passowrd(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(seconds=settings.access_token_ttl)
    }

    return jwt.encode(payload, settings.secret_token, settings.algorithm)

def validate_access_token(token: str) -> int:
    payload = jwt.decode(
        token,
        settings.secret_token,
        [settings.algorithm],
        options={"require": ["sub", "exp", "iat"]}
    )

    return int(payload["sub"])

def create_refresh_token() -> str:
    return secrets.token_hex(32)

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
