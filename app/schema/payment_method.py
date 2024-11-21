from typing import Dict

from pydantic import BaseModel, Field

from .base import TimestampMixinSchema, UuidMixinSchema


class PaymentMethodBase(BaseModel):
    type: str  # Ex: "credit_card", "boleto"
    details: Dict[str, str] | None = Field(
        default_factory=dict
    )  # Opcional, com valor padrão
    is_default: bool = False


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(BaseModel):
    type: str | None
    details: Dict[str, str] | None
    is_default: bool | None


class PaymentMethodResponse(PaymentMethodBase, UuidMixinSchema, TimestampMixinSchema):
    class Config:
        from_attributes = True
