from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import PersistableModel, TimestampMixin, UuidMixin

if TYPE_CHECKING:
    from .customer import Customer


class PaymentMethod(PersistableModel, UuidMixin, TimestampMixin):
    __tablename__ = "payment_methods"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # Ex: credit_card, boleto
    details: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )  # Armazena informações como últimos dígitos do cartão
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    customer: Mapped["Customer"] = relationship(back_populates="payment_methods")

    def __repr__(self) -> str:
        return f"<PaymentMethod(id={self.id}, type={self.type})>"
