from pydantic import BaseModel

from .base import TimestampMixinSchema, UuidMixinSchema


class AddressBase(BaseModel):
    street: str
    number: str | None
    city: str
    state: str
    postal_code: str
    country: str = "Brazil"
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: str | None
    number: str | None
    city: str | None
    state: str | None
    postal_code: str | None
    country: str | None
    is_default: bool | None


class AddressResponse(AddressBase, UuidMixinSchema, TimestampMixinSchema):
    class Config:
        from_attributes = True
