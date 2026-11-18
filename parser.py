# receita de bolo com o dedo marcado no passo que eu estou 
#ista de tokens que o scan já entrega e um dedo apontando para um deles
from tokens import Token, TokenType
from erros import ErroSintatico
from arvore import Numero, Variavel, Operacao, Imprimir, Atribuicao, Enquanto, Bloco, Se

class Parser:

    def __init__(self,tokens,pos=0):
        self.tokens = tokens
        self.pos = pos

    def olhar(self):
        return self.tokens[self.pos]

    def avancar(self):
        self.token_lido = self.tokens[self.pos]
        if self.token_lido.tipo != TokenType.EOF:
            self.pos += 1
        return self.token_lido

    def esperar(self, tipo_esperado, lexema_esperado = None):
        token_analizando = self.olhar()
        if (token_analizando.tipo != tipo_esperado or
        (lexema_esperado is not None and token_analizando.lexema != lexema_esperado)):

            if token_analizando.tipo == TokenType.EOF:
                if lexema_esperado is not None:
                    descricao = f"Fim de arquivo inesperado. Esperava-se '{lexema_esperado}'."
                else:
                    descricao = f"Fim de arquivo inesperado. Esperava-se '{tipo_esperado.name}'."

            elif lexema_esperado is not None:
                descricao = f"Esperava-se '{lexema_esperado}', mas veio '{token_analizando.lexema}'."

            else:
                descricao = f"Esperava-se '{tipo_esperado.name}', mas veio '{token_analizando.tipo.name}'."

            raise ErroSintatico(descricao, token_analizando.linha)

        return self.avancar()



    def expressao(self):
        #caso int e float
        token_atual = self.olhar()
        if token_atual.tipo in (TokenType.INT, TokenType.FLOAT):
            token_consumido = self.avancar()
            numero = Numero(token_consumido.lexema, token_consumido.linha)

            return numero

        elif token_atual.tipo == TokenType.IDENTIFIER:
            token_consumido = self.avancar()
            nome = Variavel(token_consumido.lexema, token_consumido.linha)

            return nome

        elif token_atual.tipo == TokenType.DELIMITER and token_atual.lexema == '(':
            self.esperar(TokenType.DELIMITER, '(')

            operador = self.esperar(TokenType.OPERATOR)

            esquerda = self.expressao()
            direita = self.expressao()

            self.esperar(TokenType.DELIMITER, ')')
            return Operacao(operador.lexema, esquerda, direita, operador.linha)

        if token_atual.tipo == TokenType.EOF:
            descricao = "Fim de arquivo inesperado. Esperava-se uma expressão."
        else:
            descricao = f"Esperava-se uma expressão, mas veio '{token_atual.lexema}'."

        raise ErroSintatico(descricao, token_atual.linha)

    def comando(self):
        self.esperar(TokenType.DELIMITER, '(')
        token_atual = self.olhar()
        if token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'print':
            palavra = self.esperar(TokenType.KEYWORD)
            expressao = self.expressao()
            self.esperar(TokenType.DELIMITER, ')')
            return Imprimir(expressao, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'set':
            nome = self.esperar(TokenType.KEYWORD)
            nome = self.esperar(TokenType.IDENTIFIER)
            expressao = self.expressao()
            self.esperar(TokenType.DELIMITER, ')')
            return Atribuicao(nome.lexema,expressao, nome.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'while':
            palavra = self.esperar(TokenType.KEYWORD)
            condicao = self.expressao()
            corpo = self.comando()
            self.esperar(TokenType.DELIMITER, ')')
            return Enquanto(condicao , corpo, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'if':
            palavra = self.esperar(TokenType.KEYWORD)
            condicao = self.expressao()
            verdadeiro = self.comando()
            
            token_proximo =  self.olhar()
            if token_proximo.tipo == TokenType.DELIMITER and token_proximo.lexema == ')':
                raise ErroSintatico(descricao = "Estrutura 'if' malformada. Omitido argumento de 'else'.")
            else:
                falso = self.comando()
            
            self.esperar(TokenType.DELIMITER, ')')

            return Se(condicao, verdadeiro, falso, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'begin':
            palavra = self.esperar(TokenType.KEYWORD)
            token_atual = self.olhar()   # Sem a foto 1, na primeira pergunta o token_atual ainda é o begin, o laço entra, e o comando() encontra o ) do (begin) onde esperava um (.
            comandos = []
            while(token_atual.tipo != TokenType.EOF and not (token_atual.tipo == TokenType.DELIMITER and token_atual.lexema == ')')):
                esperando = self.comando()
                comandos.append(esperando)
                token_atual = self.olhar()
            self.esperar(TokenType.DELIMITER, ')')

            return Bloco(comandos, palavra.linha)
        
        descricao = f"Esperava-se um comando (print, set, if, while ou begin), mas veio '{token_atual.lexema}'."


        raise ErroSintatico(descricao, token_atual.linha)

    def programa(self):
        comandos = []
        while (self.olhar().tipo != TokenType.EOF):     
            comandos.append(self.comando())
        return comandos

            

         
    






