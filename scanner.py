
from tokens import Token, TokenType
from erros import ErroLexico
import string


PALAVRAS_RESERVADAS = {
    'if', 'while', 'set', 'begin', 'print'
}

PERMITIDOS = string.ascii_letters + "_" + "0123456789"

INICIO = string.ascii_letters + "_"


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
            self.linha += 1

        try:
            self.atual = self.proximo
            self.proximo = next(self.iterador)
        except StopIteration:
            self.atual = self.proximo
            self.proximo = None

    def ler_digitos(self):
        numeros = ''

        while self.atual is not None and self.atual in '0123456789':
            numeros += self.atual
            self.avancar()

        return numeros

    def ler_identificador(self):
        caractere = ''

        while self.atual is not None and self.atual in PERMITIDOS:
            caractere += self.atual
            self.avancar()

        return caractere

    def scan(self):

        tokens = []

        while self.atual is not None:

            if self.atual in ('\n', '\t', ' ', '\r'):
                self.avancar()

            elif self.atual in (')', '('):
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.DELIMITER, lexema, self.linha))

            elif self.atual in ('+', '-', '*', '/', '%'):
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.OPERATOR, lexema, self.linha))

            elif self.atual is not None and self.atual in '0123456789':

                linha_inicio = self.linha
                parte_inteira = self.ler_digitos()

                if self.atual == '.':
                    if self.proximo is not None and self.proximo in '0123456789':
                        self.avancar()
                    else:
                        raise ErroLexico(self.atual, self.linha)

                    parte_decimal = self.ler_digitos()

                    lexema = parte_inteira + '.' + parte_decimal

                    tokens.append(Token(TokenType.FLOAT, lexema, linha_inicio))

                else:
                    tokens.append(Token(TokenType.INT, parte_inteira, linha_inicio))

            elif self.atual is not None and self.atual in INICIO:

                linha_inicio = self.linha
                ler_palavra = self.ler_identificador()

                if ler_palavra in PALAVRAS_RESERVADAS:
                    tokens.append(Token(TokenType.KEYWORD, ler_palavra, linha_inicio))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, ler_palavra, linha_inicio))

            else:
                raise ErroLexico(self.atual, self.linha)

        lexema = ""
        tokens.append(Token(TokenType.EOF, lexema, self.linha))

        return tokens
