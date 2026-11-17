
from scanner import Scanner
from erros import ErroLexico
from tokens import TokenType



testes = [
    ("print", "KEYWORD"),
    ("contador", "IDENTIFIER"),
    ("a", "IDENTIFIER"),
    ("iffy", "IDENTIFIER"),
    ("(set a 10)", "TOKENS"),
    ("maçã", "ERRO"),
    ("@a", "ERRO")
]

for entrada, esperado in testes:
    print(f"\nEntrada: {entrada}")

    try:
        scanner = Scanner(entrada)
        tokens = scanner.scan()

        if esperado == "TOKENS":
            for token in tokens:
                print(token)

        elif esperado == "KEYWORD":
            assert tokens[0].tipo == TokenType.KEYWORD
            print("PASSOU:", tokens)

        elif esperado == "IDENTIFIER":
            assert tokens[0].tipo == TokenType.IDENTIFIER
            print("PASSOU:", tokens)

        else:
            print("FALHOU: deveria gerar erro léxico")

    except ErroLexico as erro:
        if esperado == "ERRO":
            print("PASSOU: erro léxico identificado")
            print(erro)
        else:
            print("FALHOU:", erro)

    except Exception as erro:
        print("ERRO NO TESTE:", erro)