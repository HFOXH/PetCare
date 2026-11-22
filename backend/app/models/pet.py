import uuid

from datetime import date

from sqlalchemy import (
    String,
    Date,
    Float,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Pet(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "pets"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    breed: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    sex: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    weight: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    species_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("species.id"),
        nullable=False
    )

    owner: Mapped["User"] = relationship(
        back_populates="pets"
    )

    species: Mapped["Species"] = relationship(
        back_populates="pets"
    )

    vaccinations: Mapped[list["PetVaccination"]] = relationship(
        back_populates="pet",
        cascade="all, delete-orphan"
    )
