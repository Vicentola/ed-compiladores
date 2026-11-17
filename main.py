

from tokens import TokenType
from scanner import Scanner
from erros import ErroLexico


def main():
    s = Scanner()
   
    try:
        tokens = s.scan('@')

    except ErroLexico as erro:
        print(erro)

    else:
        print("nao tem erros")
        print(tokens)

if __name__ == '__main__':
    main()



    

