from scanner import Scanner
from parser import Parser
from erros import ErroLexico, ErroSintatico


def rodar(texto):
    return Parser(Scanner(texto).scan()).programa()


# (nome, entrada, esperado)
# esperado = nome da classe do 1º comando  OU  um pedaço da mensagem de erro
testes = [
    ("print simples",        "(print 10)",                              "Imprimir"),
    ("set",                  "(set a 10)",                              "Atribuicao"),
    ("operacao aninhada",    "(print (+ 1 (* 2 3)))",                   "Imprimir"),
    ("if com else",          "(if (>= a 18) (print 1) (print 0))",      "Se"),
    ("while",                "(while (> a 0) (print a))",               "Enquanto"),
    ("begin",                "(begin (print 1) (print 2))",             "Bloco"),
    ("begin vazio",          "(begin)",                                 "Bloco"),
    ("dois comandos",        "(print 1)\n(print 2)",                    "Imprimir"),

    ("parentese aberto",     "(print 10",         "Fim de arquivo inesperado. Esperava-se ')'"),
    ("if sem else",          "(if (>= a 18) (print 1))",  "Omitido argumento de 'else'"),
    ("comando desconhecido", "(foo 1)",           "comando"),
    ("parentese solto",      ")",                 "Esperava-se '('"),
    ("expressao faltando",   "(print)",           "expressão"),
    ("caractere invalido",   "(print 1)\n(print 2)\n(print @)",  "'@' na linha 3"),
]

ok = 0
for nome, texto, esperado in testes:
    try:
        resultado = rodar(texto)
        tipo = type(resultado[0]).__name__ if resultado else "(vazio)"
        passou = tipo == esperado
        detalhe = f"veio {tipo}"
    except (ErroLexico, ErroSintatico) as erro:
        passou = esperado in str(erro)
        detalhe = f"erro: {erro}"
    ok += passou
    print(("OK   " if passou else "FALHA"), nome, "->", detalhe)

print(f"\n{ok}/{len(testes)} passaram")