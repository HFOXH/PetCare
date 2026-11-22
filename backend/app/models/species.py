from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Species(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "species"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    pets: Mapped[list["Pet"]] = relationship(
        back_populates="species"
    )

    vaccines: Mapped[list["Vaccine"]] = relationship(
        back_populates="species"
    )
