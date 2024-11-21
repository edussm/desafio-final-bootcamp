from datetime import datetime
from typing import TypeAlias
from uuid import UUID as UuidType

from pydantic import BaseModel

ModelSchema: TypeAlias = BaseModel


# Pydantic Mixins
class UuidMixinSchema(BaseModel):
    id: UuidType = None


class TimestampMixinSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
