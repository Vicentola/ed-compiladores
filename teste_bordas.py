from scanner import Scanner
from erros import ErroLexico

# (entrada, esperado): lista de tipos de token, ou ("ERRO", caractere)
casos = [
    ("10",       ["INT", "EOF"]),
    ("3.14",     ["FLOAT", "EOF"]),
    ("3.",       ("ERRO", ".")),
    (".5",       ("ERRO", ".")),
    ("3.14.15",  ("ERRO", ".")),
    ("(- 0 5)",  ["DELIMITER", "OPERATOR", "INT", "INT", "DELIMITER", "EOF"]),
    ("<=",       ["OPERATOR", "EOF"]),
    ("=",        ("ERRO", "=")),
    ("!",        ("ERRO", "!")),
    ("café",     ("ERRO", "é")),
    ("",         ["EOF"]),
    ("a_b1",     ["IDENTIFIER", "EOF"]),
]

ok = 0
for texto, esperado in casos:
    try:
        tipos = [t.tipo.name for t in Scanner(texto).scan()]
        passou = tipos == esperado
        detalhe = tipos
    except ErroLexico as erro:
        passou = esperado == ("ERRO", erro.caractere)
        detalhe = f"ERRO {erro.caractere!r}"
    ok += passou
    print("OK   " if passou else "FALHA", repr(texto), "->", detalhe)

print(f"\n{ok}/{len(casos)} passaram")