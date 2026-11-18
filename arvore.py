
from dataclasses import dataclass


@dataclass
class Numero:
    valor: str
    linha: int

@dataclass
class Variavel:
    nome: str
    linha: int

@dataclass
class Operacao:
    operador: str
    esquerda: object
    direita: object
    linha: int

no = Operacao("+", Numero("1", 1), Variavel("a", 1), 1)
print(no)

@dataclass
class Imprimir:
    expressao: object
    linha: int 

@dataclass
class Atribuicao:
    nome: str
    expressao: object
    linha: int

@dataclass
class Se:
    condicao: object
    verdadeiro: object
    falso: object
    linha: int

@dataclass
class Enquanto:
    condicao: object
    comando: object
    linha: int

@dataclass
class Bloco:
    comandos: list
    linha: int



