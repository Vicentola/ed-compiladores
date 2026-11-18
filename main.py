import sys

from scanner import Scanner
from parser import Parser
from erros import ErroLexico, ErroSintatico


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        return

    caminho = sys.argv[1]

    try:
        with open(caminho, 'r', encoding='utf-8-sig') as arquivo:
            texto = arquivo.read()

        tokens = Scanner(texto).scan()
        comandos = Parser(tokens).programa()

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")

    except (ErroLexico, ErroSintatico) as erro:
        print(erro)

    else:
        print(comandos)


if __name__ == '__main__':
    main()




    

