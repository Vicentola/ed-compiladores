from tokens import Token, TokenType
from erros import ErroLexico

class Scanner:
    def __init__(self, text) -> None:
        self.iterador = iter(text)
        self.atual = None
        self.proximo = None
        self.linha = 1
        self.avancar()
        self.avancar()

    def avancar(self):

        if self.atual == '\n':
            self.linha +=1

        try:
            self.atual =  self.proximo
            self.proximo = next(self.iterador)
        except StopIteration:
            self.proximo = None
            
            
           

    def scan(self):
        tokens = []
        while self.atual is not None:
            if self.atual in ('\n', '\t', ' ', '\r'):
                self.avancar()
            
            
            elif self.atual in (')','('):
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.DELIMITER, lexema, self.linha))

            elif self.atual in ('+','-','*','/','%'):
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.OPERATOR, lexema, self.linha))          

        



            else:
                raise ErroLexico(self.atual, self.linha)   
            
            
            
        lexema = ""
        tokens.append(Token(TokenType.EOF, lexema,self.linha))
            
        return tokens

    

