from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Главный класс настроек, который читает переменные окружения и .env
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Minecraft Server API"  # Человекочитаемое имя сервиса
    ENV: str = "dev"  # Текущий режим работы: dev/prod/test
    DEBUG: bool = True  # Флаг отладки

    API_HOST: str  # Адрес, на котором слушает API
    API_PORT: int = 8000  # Порт HTTP-сервера по умолчанию

    # Разрешённые фронтенд-домен(ы) для CORS, чтобы браузер не блочил запросы
    CORS_ORIGINS: list[str]

    SECRET_KEY: str  # Секретный ключ
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Время жизни access-токена в минутах

    # Полная строка подключения к БД
    DATABASE_URL: str

    # Адрес Redis
    REDIS_URL: str | None = None

    # Minecraft settings
    MINECRAFT_HOST: str
    MINECRAFT_PORT: int | None = None
    MINECRAFT_RCON_PORT: int | None = None
    MINECRAFT_RCON_PASSWORD: str | None = None

    # Telegram settings
    TELEGRAM_BOT_TOKEN: str | None = None
    TELEGRAM_CHAT_ID: str | None = None


settings = Settings()  # type: ignore[call-arg]
