from typing import Optional
from pydantic import BaseModel, Field


class RecordModel(BaseModel):
    """
    DTO padrão para representar um registro da API.
    Pode ser adaptado conforme o endpoint usado.
    """

    id: int = Field(..., description="ID único do registro")
    nome: str = Field(..., description="Nome da unidade federativa")
    sigla: Optional[str] = Field(None, description="Sigla do estado")
    regiao: Optional[dict] = Field(None, description="Região do estado")

    class Config:
        extra = "ignore"   # Ignora campos desnecessários
        validate_assignment = True
        from_attributes = True
