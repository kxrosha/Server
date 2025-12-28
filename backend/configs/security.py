from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from passlib.context import CryptContext

from configs.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


# принимает обычный пароль и возвращает ero хеш через bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# берёт введённый пароль и хеш из базы, сравнивает их и отвечает, верный пароль или нет
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# генерирует JWT-токен
def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
