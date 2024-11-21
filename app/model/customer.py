import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.database import Base

from .base import TimestampMixin, UuidMixin

if TYPE_CHECKING:
    from .address import Address
    from .payment_method import PaymentMethod


class CustomerType(str, enum.Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"


class Customer(Base, UuidMixin, TimestampMixin):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    document: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )  # CPF ou CNPJ
    type: Mapped[CustomerType] = mapped_column(
        Enum(CustomerType), default=CustomerType.INDIVIDUAL, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamentos
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan", lazy="selectin"
    )
    payment_methods: Mapped[list["PaymentMethod"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"
