class ErroLexico(Exception):
    def __init__(self, caractere, linha):
        self.caractere = caractere
        self.linha = linha

        super().__init__(
            f"Erro léxico '{caractere}' na linha {linha}"
        )