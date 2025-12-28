from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from configs.settings import settings


# Базовый класс для всех ORM-моделей
class Base(DeclarativeBase):
    pass


# engine - объект подключения к БД
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    future=True,
)

# Фабрика сессий, которую будем использовать в dependency
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# Dependency-функция для FastAPI, которая отдаёт сессию БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
