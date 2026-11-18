from scanner import Scanner
from parser import Parser
from erros import ErroLexico, ErroSintatico


def rodar(texto):
    return Parser(Scanner(texto).scan()).programa()


POSITIVOS = [
    ("1) print basico", "(print 10)"),
    ("2) operacoes", """(begin
  (print (+ 10 (* 3 5)))
  (print (- 100 (/ 20 2)))
)"""),
    ("3) variaveis", """(begin
  (set a 10)
  (set b 20)
  (print (+ a b))
)"""),
    ("4) condicional", """(begin
  (set idade 20)
  (if (>= idade 18)
       (print 1)
       (print 0)
  )
)"""),
    ("5) repeticao", """(begin
  (set contador 1)
  (while (<= contador 10)
    (begin
       (print contador)
       (set contador (+ contador 1))
    )
  )
)"""),
    ("(erro semantico e do amigo; aqui so parseia)", "(print a)"),
]

NEGATIVOS = [
    ("1) erro lexico", """(begin
  (set valor 100)
  (print (valor @ 2)))""",
     "Erro Léxico: Caractere inválido '@' na linha 3."),
    ("2) parentese nao fechado", """(begin
  (print (+ 1 2)
)""",
     "Erro Sintático na linha 2: Fim de arquivo inesperado. Esperava-se ')'."),
    ("3) if sem else", "(if (> x 10) (print 1))",
     "Erro Sintático: Estrutura 'if' malformada. Omitido argumento de 'else'."),
]

print("=== POSITIVOS (devem parsear sem erro) ===")
for nome, texto in POSITIVOS:
    try:
        cmds = rodar(texto)
        print("OK   ", nome, "->", [type(c).__name__ for c in cmds])
    except (ErroLexico, ErroSintatico) as erro:
        print("FALHA", nome, "->", erro)

print("\n=== NEGATIVOS (mensagem exata do PDF) ===")
for nome, texto, esperado in NEGATIVOS:
    try:
        rodar(texto)
        print("FALHA", nome, "-> nao deu erro")
    except (ErroLexico, ErroSintatico) as erro:
        if str(erro) == esperado:
            print("OK   ", nome)
        else:
            print("FALHA", nome)
            print("   veio:    ", erro)
            print("   esperado:", esperado)