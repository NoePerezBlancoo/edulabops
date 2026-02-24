from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .settings import settings

ph = PasswordHasher()

def hash_password(p: str) -> str:
    return ph.hash(p)

def verify_password(p: str, h: str) -> bool:
    try:
        return ph.verify(h, p)
    except VerifyMismatchError:
        return False

def create_token(sub: str, role: str, minutes: int = 60 * 24) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": sub, "role": role, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=minutes)).timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError as e:
        raise ValueError("invalid_token") from e