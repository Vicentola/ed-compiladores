
from scanner import Scanner
from erros import ErroLexico
from tokens import TokenType




testes = [
    "=",
    "(= 1 2)",
    "<!",
    "=!",
    "(<= 1 2)",
    "print\n(set a 10)"
]

for texto in testes:
    print(f"\nEntrada: {repr(texto)}")

    try:
        scanner = Scanner(texto)
        tokens = scanner.scan()

        for token in tokens:
            print(token)

    except ErroLexico as erro:
        print(erro)
