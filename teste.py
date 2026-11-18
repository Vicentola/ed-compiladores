
from scanner import Scanner
from erros import ErroLexico
from tokens import TokenType
from erros import ErroSintatico
from parser import Parser
from arvore import Atribuicao, Imprimir, Se, Enquanto, Bloco


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




try:
    raise ErroSintatico("Fim de arquivo inesperado. Esperava-se ')'.", 2)
except ErroSintatico as erro:
    print(erro)

try:
    raise ErroSintatico("Estrutura 'if' malformada. Omitido argumento de 'else'.")
except ErroSintatico as erro:
    print(erro)



codigo = "(print 10)"

scanner = Scanner(codigo)
tokens = scanner.scan()

parser = Parser(tokens)

while parser.olhar().tipo != TokenType.EOF:
    print("Olhar:", parser.olhar())

    token = parser.avancar()
    print("Consumido:", token)

# Testando o EOF
print("Olhar:", parser.olhar())

parser.avancar()

print("Após avançar no EOF:", parser.olhar())

from scanner import Scanner
from parser import Parser
from tokens import TokenType

codigo = "(print 10)"

# 1. Gerar tokens
scanner = Scanner(codigo)
tokens = scanner.scan()

# 2. Criar o Parser
parser = Parser(tokens)

# 3. Testar o primeiro token
try:
    token = parser.esperar(TokenType.DELIMITER)
    print("Resultado 1:", token)
except ErroSintatico as erro:
    print(erro)

# 4. Testar o próximo token
try:
    token = parser.esperar(TokenType.INT)
    print("Resultado 2:", token)
except ErroSintatico as erro:
    print("Resultado 2:", erro)


parser = Parser(tokens)   # tokens já gerados lá em cima, parser novo (pos = 0)

parser.esperar(TokenType.DELIMITER)   # consome (
parser.esperar(TokenType.KEYWORD)     # consome print

print("pos antes:", parser.pos)

try:
    parser.esperar(TokenType.DELIMITER)   # no 10: deve dar erro
except ErroSintatico as erro:
    print(erro)


from arvore import Numero, Variavel

parser = Parser(Scanner("10").scan())
print(parser.expressao())

parser = Parser(Scanner("a").scan())
print(parser.expressao())


parser = Parser(Scanner("(+ 1 a)").scan())
print(parser.expressao())

parser = Parser(Scanner("(+ 1 (* 2 3))").scan())
print(parser.expressao())

codigo = "(+ 1 2"

try:
    tokens = Scanner(codigo).scan()
    parser = Parser(tokens)
    resultado = parser.expressao()
    print(resultado)

except ErroSintatico as erro:
    print(erro)

codigo = ")"

try:
    tokens = Scanner(codigo).scan()
    parser = Parser(tokens)
    resultado = parser.expressao()
    print(resultado)

except ErroSintatico as erro:
    print(erro)


codigo = ""

try:
    tokens = Scanner(codigo).scan()
    parser = Parser(tokens)
    resultado = parser.expressao()
    print(resultado)

except ErroSintatico as erro:
    print(erro)

print(Imprimir(Numero("10", 1), 1))
print(Atribuicao("a", Numero("10", 1), 1))


parser = Parser(Scanner("(print 10)").scan())
print(parser.comando())
parser = Parser(Scanner("(print (+ 1 2))").scan())
print(parser.comando())

parser = Parser(Scanner("(set a 10)").scan())
print(parser.comando())



print(Se(Numero("1", 1), Imprimir(Numero("1", 1), 1), Imprimir(Numero("0", 1), 1), 1))
print(Enquanto(Numero("1", 1), Imprimir(Numero("1", 1), 1), 1))
print(Bloco([Imprimir(Numero("1", 1), 1)], 1))