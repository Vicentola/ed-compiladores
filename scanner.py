
# Analisador léxico (scanner): transforma o texto do programa em uma lista de tokens.
# É uma máquina de estados escrita à mão: olha o caractere atual e, usando o próximo
# (lookahead), decide qual token está sendo lido. Para no primeiro caractere inválido.

from tokens import Token, TokenType
from erros import ErroLexico
import string


# Palavras que viram KEYWORD. Um identificador cujo texto está aqui deixa de ser IDENTIFIER.
PALAVRAS_RESERVADAS = {
    'if', 'while', 'set', 'begin', 'print'
}

# Caracteres permitidos DENTRO de um identificador: letras ASCII, '_' e dígitos.
PERMITIDOS = string.ascii_letters + "_" + "0123456789"

# Caracteres que podem COMEÇAR um identificador (não pode começar com dígito).
INICIO = string.ascii_letters + "_"


# Percorre o texto um caractere por vez, guardando sempre dois: 'atual' (o que está sendo lido)
# e 'proximo' (uma espiada à frente, o lookahead). Método principal: scan().
class Scanner:

    def __init__(self, text) -> None:
        # iter(text) entrega o texto um caractere por vez, sem usar índices.
        self.iterador = iter(text)
        # Começam vazios; as duas chamadas a avancar() mais abaixo preenchem os dois.
        self.atual = None
        self.proximo = None
        # Contador de linhas, usado nas mensagens de erro. Começa na linha 1.
        self.linha = 1
        # A 1ª chamada coloca o 1º caractere em 'proximo'; a 2ª o passa para 'atual' e lê o 2º.
        self.avancar()
        self.avancar()

    # Anda um caractere: 'proximo' vira 'atual' e lê-se um novo 'proximo'.
    def avancar(self):

        # A linha só sobe quando o '\n' SAI de 'atual'; por isso o caractere seguinte já conta como linha nova.
        if self.atual == '\n':
            self.linha += 1

        # No fim do texto, next() levanta StopIteration: 'proximo' vira None (não há mais caracteres).
        try:
            self.atual = self.proximo
            self.proximo = next(self.iterador)
        # 'atual' recebe o último caractere que sobrou; na chamada seguinte recebe None, o que encerra o laço do scan().
        except StopIteration:
            self.atual = self.proximo
            self.proximo = None

    # Lê dígitos seguidos e devolve o texto lido (usado por INT e FLOAT). Para no 1º caractere que não é dígito.
    def ler_digitos(self):
        numeros = ''

        # O teste 'is not None' é necessário: no fim do texto 'atual' é None, e 'None in ...' daria erro.
        while self.atual is not None and self.atual in '0123456789':
            numeros += self.atual
            self.avancar()

        return numeros

    # Lê letras, '_' e dígitos seguidos e devolve o texto do identificador.
    def ler_identificador(self):
        caractere = ''

        while self.atual is not None and self.atual in PERMITIDOS:
            caractere += self.atual
            self.avancar()

        return caractere

    # Lê o texto inteiro e devolve a lista de tokens, sempre terminada em EOF.
    def scan(self):

        tokens = []

        # Cada volta reconhece UM token (ou descarta um espaço). Termina quando o texto acaba ('atual' vira None).
        while self.atual is not None:

            if self.atual in ('\n', '\t', ' ', '\r'):
                # Espaço em branco: descartado, não gera token. O '\r' dos arquivos do Windows (\r\n) também é ignorado.
                self.avancar()

            elif self.atual in (')', '('):
                # Delimitadores: '(' e ')', um caractere cada.
                # A linha é lida depois do avancar(), mas como '(' e ')' não são quebra de linha, continua certa.
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.DELIMITER, lexema, self.linha))

            elif self.atual in ('+', '-', '*', '/', '%'):
                # Operadores de um caractere só: + - * / %.
                lexema = self.atual
                self.avancar()
                tokens.append(Token(TokenType.OPERATOR, lexema, self.linha))


            elif self.atual in ('<', '>', '=', '!'):
                # Operadores que podem ter dois caracteres: <, >, <=, >=, == e !=.
                # Guarda a linha onde o operador começa.
                linha_inicio = self.linha
                lexema = self.atual

                # Lookahead: se o próximo é '=', o operador tem dois caracteres (<=, >=, == ou !=).
                if self.proximo == '=':
                    lexema += self.proximo
                    self.avancar()

                self.avancar()

                # Consumiu o último caractere do operador. '=' e '!' sozinhos não são válidos:
                # a atribuição é feita pelo 'set' e a igualdade pelo '=='.
                if lexema in ('!', '='):
                    raise ErroLexico(lexema, linha_inicio)

                tokens.append(Token(TokenType.OPERATOR, lexema, linha_inicio))



            elif self.atual is not None and self.atual in '0123456789':
                # Número: começa com dígito. É INT se acaba nos dígitos, ou FLOAT se tem '.' seguido de dígito.

                linha_inicio = self.linha
                # Lê os dígitos antes do ponto (ou o número inteiro, se não houver ponto).
                parte_inteira = self.ler_digitos()

                # Achou um ponto: só é FLOAT se houver um dígito logo depois.
                if self.atual == '.':
                    if self.proximo is not None and self.proximo in '0123456789':
                        self.avancar()
                    else:
                        # Ponto sem dígito depois ('3.' ou '3.x') é erro léxico.
                        raise ErroLexico(self.atual, self.linha)

                    # Lê os dígitos depois do ponto.
                    parte_decimal = self.ler_digitos()

                    lexema = parte_inteira + '.' + parte_decimal

                    tokens.append(Token(TokenType.FLOAT, lexema, linha_inicio))

                else:
                    # Não tinha ponto: é um INT.
                    tokens.append(Token(TokenType.INT, parte_inteira, linha_inicio))

            elif self.atual is not None and self.atual in INICIO:
                # Identificador ou palavra reservada: começa com letra ou '_'.

                linha_inicio = self.linha
                ler_palavra = self.ler_identificador()

                # Lê como identificador e depois consulta a lista de palavras reservadas.
                if ler_palavra in PALAVRAS_RESERVADAS:
                    tokens.append(Token(TokenType.KEYWORD, ler_palavra, linha_inicio))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, ler_palavra, linha_inicio))

            else:
                # Qualquer outro caractere (por exemplo '@' ou ';') não pertence à linguagem: erro léxico.
                raise ErroLexico(self.atual, self.linha)

        # O token EOF marca o fim da lista. A linha dele é a do último token real, para que o erro de
        # 'fim de arquivo' não dependa de haver uma quebra de linha no final do arquivo.
        if tokens:
            linha_eof = tokens[-1].linha
        else:
            linha_eof = self.linha

        lexema = ""
        tokens.append(Token(TokenType.EOF, lexema, linha_eof))

        # Lista completa de tokens, sempre terminada em EOF.
        return tokens
