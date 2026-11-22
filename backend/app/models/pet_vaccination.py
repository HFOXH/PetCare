import uuid

from datetime import date

from sqlalchemy import (
    Date,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class PetVaccination(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "pet_vaccinations"

    pet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    vaccine_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vaccines.id"),
        nullable=False
    )

    administered_at: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    next_due_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    veterinarian: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    pet: Mapped["Pet"] = relationship(
        back_populates="vaccinations"
    )

    vaccine: Mapped["Vaccine"] = relationship(
        back_populates="pet_vaccinations"
    )
