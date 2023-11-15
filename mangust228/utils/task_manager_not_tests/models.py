from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime
from datetime import datetime
from .db import engine


class Base(DeclarativeBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TaskModel(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    url: Mapped[str] = mapped_column(unique=True, index=True)
    retries: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    done: Mapped[bool] = mapped_column(default=False)
    result_url: Mapped[str] = mapped_column(nullable=True, default=None)
    reason: Mapped[str] = mapped_column(default=None, nullable=True)


Base.metadata.create_all(engine)
