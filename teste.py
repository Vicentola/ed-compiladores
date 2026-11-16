
from scanner import Scanner
from erros import ErroLexico


def testar_delimitadores():
    print("=== TESTE DELIMITADORES E EOF ===")

    scanner = Scanner("()")

    try:
        tokens = scanner.scan()

        for token in tokens:
            print(
                f"Tipo: {token.tipo.name} | "
                f"Lexema: {repr(token.lexema)} | "
                f"Linha: {token.linha}"
            )

    except ErroLexico as erro:
        print(erro)


def testar_caractere_invalido():
    print("\n=== TESTE CARACTERE INVÁLIDO ===")

    scanner = Scanner("( @ )")

    try:
        tokens = scanner.scan()

        for token in tokens:
            print(token)

    except ErroLexico as erro:
        print(erro)


def testar_linha_erro():
    print("\n=== TESTE LINHA DO ERRO ===")

    scanner = Scanner("(\n@)")

    try:
        tokens = scanner.scan()

        for token in tokens:
            print(token)

    except ErroLexico as erro:
        print(erro)


if __name__ == '__main__':
    testar_delimitadores()
    testar_caractere_invalido()
    testar_linha_erro()
