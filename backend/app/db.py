from sqlmodel import create_engine, Session

from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session
