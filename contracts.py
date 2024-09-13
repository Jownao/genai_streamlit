from datetime import datetime
from typing import Tuple
from pydantic import BaseModel, EmailStr, PositiveFloat, PositiveInt
from enum import Enum

class ProdutoEnum(str, Enum):
    produto1 = "Inteligência com Gemini"
    produto2 = "Inteligência com chatGPT"
    produto3 = "Inteligência com Llama3.0"

class Vendas(BaseModel):
    """
    Modelo de dados para as vendas.
        email (EmailStr): email do comprador
        data (datetime): data da compra
        valor (PositiveFloat): valor da compra
        produto (PositiveInt): nome do produto
        quantidade (PositiveInt): quantidade de produtos
        produto (ProdutoEnum): categoria do produto
    """
    email: EmailStr 
    data: datetime
    valor: PositiveFloat 
    quantidade: PositiveInt
    produto: ProdutoEnum

    