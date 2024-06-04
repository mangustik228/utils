from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class UserModel(Base):
    __tablename__ = "user"
    name: Mapped[str]
    surname: Mapped[str | None]


class RoleModel(Base):
    __tablename__ = "role"
    name: Mapped[str]