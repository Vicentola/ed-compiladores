from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    FLOAT = auto()
    INT = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    EOF = auto()
    

