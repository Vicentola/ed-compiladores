# Analisador sintático (parser): transforma a lista de tokens do scanner em uma árvore.
# É um parser descendente recursivo: cada variável da gramática (programa, comando,
# expressao) é um método, e os métodos se chamam conforme a gramática manda.
# O parser anda pela lista como um dedo marcando a posição (self.pos). Para no primeiro erro.
from tokens import Token, TokenType
from erros import ErroSintatico
from arvore import Numero, Variavel, Operacao, Imprimir, Atribuicao, Enquanto, Bloco, Se

class Parser:

    # tokens: a lista devolvida por Scanner.scan() (sempre termina em EOF). pos: posição do token atual.
    def __init__(self,tokens,pos=0):
        self.tokens = tokens
        self.pos = pos

    # Devolve o token atual SEM consumir: só espia.
    def olhar(self):
        return self.tokens[self.pos]

    # Devolve o token atual e passa para o próximo (consome).
    def avancar(self):
        self.token_lido = self.tokens[self.pos]
        # No EOF o dedo não anda: assim nunca sai da lista, e pedir mais tokens depois do fim devolve sempre o EOF.
        if self.token_lido.tipo != TokenType.EOF:
            self.pos += 1
        return self.token_lido

    # Confere o token atual: o tipo e, se for pedido, também o lexema. Se estiver certo, consome e devolve
    # o token. Se não, levanta ErroSintatico com a linha do token. É o único lugar que monta essas mensagens.
    def esperar(self, tipo_esperado, lexema_esperado = None):
        token_analizando = self.olhar()
        if (token_analizando.tipo != tipo_esperado or
        (lexema_esperado is not None and token_analizando.lexema != lexema_esperado)):

            # Deu erro. A mensagem depende do caso: fim de arquivo, lexema errado ou tipo errado.
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

        # Token correto: consome e devolve.
        return self.avancar()



    # expressao ::= NUMERO | IDENTIFICADOR | '(' OPERADOR expressao expressao ')'
    # Lê UMA expressão e devolve o nó da árvore. Decide pelo primeiro token.
    def expressao(self):
        # Olha o primeiro token para decidir o caso (sem consumir).
        # Caso 1: INT ou FLOAT -> nó Numero (o valor fica como texto).
        token_atual = self.olhar()
        if token_atual.tipo in (TokenType.INT, TokenType.FLOAT):
            token_consumido = self.avancar()
            numero = Numero(token_consumido.lexema, token_consumido.linha)

            return numero

        elif token_atual.tipo == TokenType.IDENTIFIER:
            # Caso 2: nome de variável -> nó Variavel.
            token_consumido = self.avancar()
            nome = Variavel(token_consumido.lexema, token_consumido.linha)

            return nome

        elif token_atual.tipo == TokenType.DELIMITER and token_atual.lexema == '(':
            # Caso 3: '(' abre uma operação: ( operador esquerda direita ).
            self.esperar(TokenType.DELIMITER, '(')

            operador = self.esperar(TokenType.OPERATOR)

            # Cada operando é outra expressão: a função chama a si mesma (recursão).
            # O operando pode ser número, variável ou outra operação.
            esquerda = self.expressao()
            direita = self.expressao()

            self.esperar(TokenType.DELIMITER, ')')
            return Operacao(operador.lexema, esquerda, direita, operador.linha)

        # Nenhum caso serviu: o token não começa uma expressão. Sem este erro a função devolveria None sem avisar.
        if token_atual.tipo == TokenType.EOF:
            descricao = "Fim de arquivo inesperado. Esperava-se uma expressão."
        else:
            descricao = f"Esperava-se uma expressão, mas veio '{token_atual.lexema}'."

        raise ErroSintatico(descricao, token_atual.linha)

    # comando ::= '(' set | print | if | while | begin ... ')'
    # Lê UM comando e devolve o nó da árvore. Consome o '(' e decide pela palavra reservada que vem depois.
    def comando(self):
        # Todo comando começa com '('.
        self.esperar(TokenType.DELIMITER, '(')
        token_atual = self.olhar()
        if token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'print':
            # (print expressao) -> Imprimir.
            palavra = self.esperar(TokenType.KEYWORD)
            expressao = self.expressao()
            self.esperar(TokenType.DELIMITER, ')')
            return Imprimir(expressao, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'set':
            # (set nome expressao) -> Atribuicao.
            # O 1º esperar consome a palavra 'set'; o 2º guarda o token do nome da variável.
            nome = self.esperar(TokenType.KEYWORD)
            nome = self.esperar(TokenType.IDENTIFIER)
            expressao = self.expressao()
            self.esperar(TokenType.DELIMITER, ')')
            return Atribuicao(nome.lexema,expressao, nome.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'while':
            # (while condicao comando) -> Enquanto. O corpo é um comando, por isso chama comando() de novo.
            palavra = self.esperar(TokenType.KEYWORD)
            condicao = self.expressao()
            corpo = self.comando()
            self.esperar(TokenType.DELIMITER, ')')
            return Enquanto(condicao , corpo, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'if':
            # (if condicao comando comando) -> Se. O 'else' é obrigatório.
            palavra = self.esperar(TokenType.KEYWORD)
            condicao = self.expressao()
            verdadeiro = self.comando()
            
            # Depois do ramo verdadeiro, se já vier ')' o 'else' foi omitido.
            # É o erro do enunciado; esta mensagem não leva número de linha.
            token_proximo =  self.olhar()
            if token_proximo.tipo == TokenType.DELIMITER and token_proximo.lexema == ')':
                raise ErroSintatico(descricao = "Estrutura 'if' malformada. Omitido argumento de 'else'.")
            else:
                # Ramo falso: também é um comando.
                falso = self.comando()
            
            self.esperar(TokenType.DELIMITER, ')')

            return Se(condicao, verdadeiro, falso, palavra.linha)

        elif token_atual.tipo == TokenType.KEYWORD and token_atual.lexema == 'begin':
            # (begin comando*) -> Bloco. Repete comando() até chegar no ')'.
            palavra = self.esperar(TokenType.KEYWORD)
            # Atualiza o token atual: ele ainda guarda a palavra 'begin'.
            # Sem isto, um (begin) vazio tentaria ler um comando em vez de ver o ')'.
            token_atual = self.olhar()
            comandos = []
            # Continua enquanto o token atual não for ')' nem EOF (o EOF vira erro no esperar logo abaixo).
            while(token_atual.tipo != TokenType.EOF and not (token_atual.tipo == TokenType.DELIMITER and token_atual.lexema == ')')):
                esperando = self.comando()
                comandos.append(esperando)
                # Olha de novo: o laço precisa do token de agora, e não do da volta anterior.
                token_atual = self.olhar()
            self.esperar(TokenType.DELIMITER, ')')

            return Bloco(comandos, palavra.linha)
        
        # Nenhum comando reconhecido: a palavra depois do '(' não é print, set, if, while nem begin.
        descricao = f"Esperava-se um comando (print, set, if, while ou begin), mas veio '{token_atual.lexema}'."


        raise ErroSintatico(descricao, token_atual.linha)

    # programa ::= comando*
    # Lê comandos até o fim do arquivo e devolve a lista. É a entrada do analisador semântico.
    def programa(self):
        comandos = []
        # Repete até o token atual ser o EOF; a condição olha o token de agora a cada volta.
        while (self.olhar().tipo != TokenType.EOF):     
            comandos.append(self.comando())
        return comandos

            

         
    






