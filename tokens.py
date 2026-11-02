from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    IDENTIFIER = auto()
    FLOAT = auto()
    INT = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    EOF = auto()
    
@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    

