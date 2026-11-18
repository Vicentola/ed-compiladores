import os

EXEMPLOS = {
    "positivo1.txt": "(print 10)\n",

    "positivo2.txt": """(begin
  (print (+ 10 (* 3 5)))
  (print (- 100 (/ 20 2)))
)
""",

    "positivo3.txt": """(begin
  (set a 10)
  (set b 20)
  (print (+ a b))
)
""",

    "positivo4.txt": """(begin
  (set idade 20)
  (if (>= idade 18)
       (print 1)
       (print 0)
  )
)
""",

    "positivo5.txt": """(begin
  (set contador 1)
  (while (<= contador 10)
    (begin
       (print contador)
       (set contador (+ contador 1))
    )
  )
)
""",

    "negativo1_lexico.txt": """(begin
  (set valor 100)
  (print (valor @ 2)))
""",

    "negativo2_parentese.txt": """(begin
  (print (+ 1 2)
)
""",

    "negativo3_if.txt": "(if (> x 10) (print 1))\n",

    "negativo4_semantico.txt": "(print a)\n",
}

os.makedirs("exemplos", exist_ok=True)

for nome, conteudo in EXEMPLOS.items():
    with open(os.path.join("exemplos", nome), "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("criado:", nome)