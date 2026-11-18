class ErroLexico(Exception):
    def __init__(self, caractere, linha):
        self.caractere = caractere
        self.linha = linha

        super().__init__(
            f"Erro Léxico: Caractere inválido '{caractere}' na linha {linha}."
        )

class ErroSintatico(Exception):
    def __init__(self, descricao, linha = None):
        self.descricao = descricao
        self.linha = linha

        if linha is not None:
            mensagem = f"Erro Sintático na linha {linha}: {descricao}"
        else:
            mensagem = f"Erro Sintático: {descricao}"


        super().__init__(mensagem)