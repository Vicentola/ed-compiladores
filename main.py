# Ponto de entrada: lê um arquivo Mini-LISP, roda o scanner e o parser e imprime a árvore
# ou a mensagem do primeiro erro. Uso: python main.py <arquivo>

import sys

from scanner import Scanner
from parser import Parser
from erros import ErroLexico, ErroSintatico


def main():
    # sys.argv[0] é o nome do script; sem mais nada na linha de comando, falta o caminho do arquivo.
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        return

    caminho = sys.argv[1]

    try:
        # 'utf-8-sig' descarta o marcador (BOM) que alguns editores do Windows gravam no começo do arquivo.
        with open(caminho, 'r', encoding='utf-8-sig') as arquivo:
            texto = arquivo.read()

        # Etapa 1 (léxico): texto -> lista de tokens.
        tokens = Scanner(texto).scan()
        # Etapa 2 (sintático): tokens -> lista de comandos (a árvore).
        comandos = Parser(tokens).programa()

    # O arquivo informado não existe.
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")

    # Erro do enunciado: mostra só a mensagem, sem traceback.
    except (ErroLexico, ErroSintatico) as erro:
        print(erro)

    # Sem erros: imprime a lista de comandos.
    else:
        print(comandos)


if __name__ == '__main__':
    main()




    

