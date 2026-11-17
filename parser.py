# receita de bolo com o dedo marcado no passo que eu estou 
#ista de tokens que o scan já entrega e um dedo apontando para um deles
from tokens import Token, TokenType

class Parser:

    def __init__(self,tokens,pos=0):
        self.tokens = tokens
        self.pos = pos

    def olhar(self):
        return self.tokens[self.pos]

    def avancar(self):
        self.token_lido = self.tokens[self.pos]
        if self.tipo != TokenType.EOF:
            self.pos += 1
        return self.token_lido
