from pydantic import BaseModel, Field


class PaginationQueryParams(BaseModel):
    """
    Classe para validação de parâmetros de paginação com offset e limit.
    """

    offset: int = Field(
        default=0,
        ge=0,
        description="Número de registros a serem ignorados no início. Deve ser maior ou igual a 0.",
    )
    limit: int = Field(
        default=10,
        gt=0,
        le=100,
        description="Número máximo de registros retornados. Deve ser maior que 0 e menor ou igual a 100.",
    )
