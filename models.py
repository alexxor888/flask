import datetime
import os
import atexit
from sqlalchemy import create_engine, DateTime, String, func
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase



POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class AdvertisementModel(Base):

    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    date_created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())


Base.metadata.create_all(bind=engine)

atexit.register(engine.dispose)

