
# Nós da árvore sintática. O parser cria um destes para cada construção que reconhece.
# Os parênteses não aparecem na árvore (só delimitam). Todo nó guarda a 'linha', para o
# analisador semântico poder informar erros com a posição.

from dataclasses import dataclass


# Número escrito no código. O valor fica como texto ('10', '3.14'); quem converte é o semântico ou o gerador.
@dataclass
class Numero:
    valor: str
    linha: int

# Leitura de uma variável dentro de uma expressão.
@dataclass
class Variavel:
    nome: str
    linha: int

# Operação binária: (operador esquerda direita). Os filhos podem ser Numero, Variavel ou outra Operacao.
@dataclass
class Operacao:
    operador: str
    esquerda: object
    direita: object
    linha: int



# Comando (print expressao).
@dataclass
class Imprimir:
    expressao: object
    linha: int 

# Comando (set nome expressao). 'nome' é só o texto do nome: ele recebe o valor, não é lido.
@dataclass
class Atribuicao:
    nome: str
    expressao: object
    linha: int

# Comando (if condicao verdadeiro falso). O ramo 'falso' é obrigatório.
@dataclass
class Se:
    condicao: object
    verdadeiro: object
    falso: object
    linha: int

# Comando (while condicao comando).
@dataclass
class Enquanto:
    condicao: object
    comando: object
    linha: int

# Comando (begin comando*). 'comandos' é uma lista e pode ser vazia.
@dataclass
class Bloco:
    comandos: list
    linha: int



