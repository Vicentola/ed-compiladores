# Erro do scanner: caractere que não pertence a nenhum token. Mensagem no formato do enunciado.
class ErroLexico(Exception):
    def __init__(self, caractere, linha):
        self.caractere = caractere
        self.linha = linha

        super().__init__(
            f"Erro Léxico: Caractere inválido '{caractere}' na linha {linha}."
        )

# Erro do parser. 'descricao' é o texto; 'linha' é opcional (o erro do 'if' sem 'else'
# não leva linha, como no enunciado).
class ErroSintatico(Exception):
    def __init__(self, descricao, linha = None):
        self.descricao = descricao
        self.linha = linha

        # Com linha: 'Erro Sintático na linha N: ...'. Sem linha: 'Erro Sintático: ...'.
        if linha is not None:
            mensagem = f"Erro Sintático na linha {linha}: {descricao}"
        else:
            mensagem = f"Erro Sintático: {descricao}"


        super().__init__(mensagem)