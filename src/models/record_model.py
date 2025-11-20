from typing import Optional
from pydantic import BaseModel
from src.utils.serializers import serialize_region


class RecordModel(BaseModel):
    id: int
    nome: str
    sigla: str | None = None
    regiao: dict | None = None

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sigla": self.sigla,
            "regiao": serialize_region(self.regiao),
        }
