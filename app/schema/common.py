from pydantic import BaseModel, Field


class CountResponse(BaseModel):
    count: int = Field(
        default=0,
        ge=0,
        description="Número de registros encontrados.",
    )
