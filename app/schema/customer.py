from pydantic import BaseModel, EmailStr, Field

from app.model.customer import CustomerType

from .address import AddressResponse
from .base import TimestampMixinSchema, UuidMixinSchema
from .payment_method import PaymentMethodResponse


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str | None  # Opcional
    document: str  # CPF ou CNPJ
    type: CustomerType = CustomerType.INDIVIDUAL
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = Field(None)
    email: EmailStr | None = Field(None)
    phone_number: str | None = Field(None)
    document: str | None = Field(None)
    type: CustomerType | None = Field(None)
    is_active: bool | None = Field(None)


class CustomerResponse(CustomerBase, UuidMixinSchema, TimestampMixinSchema):
    addresses: list[AddressResponse] | None = Field(default_factory=list)
    payment_methods: list[PaymentMethodResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CustomerFilterQueryParams(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Nome para busca. Deve ter entre 1 e 100 caracteres.",
    )
