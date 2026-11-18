# Compilador Mini-LISP para MEPA

Estudo Dirigido de Compiladores (UTP).

## Como rodar

python main.py exemplos/positivo1.txt

## Estrutura

- tokens.py, erros.py: tipos de token e erros
- scanner.py: analisador léxico
- parser.py, arvore.py: analisador sintático e árvore
- teste_parser.py, teste_pdf.py, teste_bordas.py: testes do parser, dos exemplos do enunciado e do léxico
- exemplos/: os programas do enunciado (positivo1 a 5 e negativo1 a 4)

## Testes

python teste_pdf.py
python teste_parser.py
python teste_bordas.py
