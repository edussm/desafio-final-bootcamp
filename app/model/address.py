from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import PersistableModel, TimestampMixin, UuidMixin

if TYPE_CHECKING:
    from .customer import Customer


class Address(PersistableModel, UuidMixin, TimestampMixin):
    __tablename__ = "addresses"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str | None] = mapped_column(String(10), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(
        String(2), nullable=False
    )  # Sigla do estado (e.g., SP, RJ)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False, default="Brazil")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    customer: Mapped["Customer"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"
