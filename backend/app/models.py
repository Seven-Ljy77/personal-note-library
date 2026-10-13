from app.database import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import String , DateTime , Boolean , Text , ForeignKey
from datetime import datetime , timezone

class User(Base) :
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    username : Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    hashed_password : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    notes : Mapped[list["Note"]] = relationship(
        back_populates="author"
    )




class Note(Base) :
    __tablename__ = "notes"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    title : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    content : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    is_pinned : Mapped[bool] = mapped_column(   # 是否置顶
        Boolean,
        default=False
    )

    author_id : Mapped[int] = mapped_column(
        ForeignKey("users.id" , ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    author : Mapped[User] = relationship(
        back_populates="notes"
    )


class RefreshToken(Base) :
    __tablename__ = "refreshtokens"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    hashed_refreshtoken : Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    user_id : Mapped[int] = mapped_column(
       ForeignKey("users.id" , ondelete="CASCADE"),
       nullable=False
    )

    expire_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=True
    )