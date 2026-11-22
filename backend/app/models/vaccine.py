import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Vaccine(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "vaccines"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    species_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("species.id"),
        nullable=False
    )

    species: Mapped["Species"] = relationship(
        back_populates="vaccines"
    )

    pet_vaccinations: Mapped[list["PetVaccination"]] = relationship(
        back_populates="vaccine"
    )
