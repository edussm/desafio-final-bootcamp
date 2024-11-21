from datetime import datetime
from typing import TypeAlias
from uuid import UUID as UuidType

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID as UuidColumn
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import FunctionElement
from uuid6 import uuid7

from app.utils.database import Base

# Some generic types for the SQLAlchemy
PersistableModel: TypeAlias = Base


# SQL Alchemy Mixins
class UuidMixin:
    id: Mapped[UuidType] = mapped_column(
        "id",
        UuidColumn(as_uuid=True),
        primary_key=True,
        default=uuid7,
        nullable=False,
        sort_order=-1000,
    )


class utcnow(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=utcnow(),
        sort_order=9999,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        server_default=utcnow(),
        server_onupdate=utcnow(),
        sort_order=10000,
    )
