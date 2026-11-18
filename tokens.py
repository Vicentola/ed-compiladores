from enum import Enum, auto


# Tipos de token que o scanner reconhece. auto() numera cada um automaticamente.
class TokenType(Enum):
    IDENTIFIER = auto()
    FLOAT = auto()
    INT = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    # Marca o fim do texto; é sempre o último token da lista.
    EOF = auto()
    
from dataclasses import dataclass

# Um token: o tipo, o texto exato que foi lido (lexema) e a linha onde ele começa.
@dataclass
class Token:
    tipo: TokenType
    lexema: str
    linha: int