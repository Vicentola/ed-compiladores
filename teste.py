from scanner import Scanner

scanner = Scanner("a\n\nb")

print("Após criar o Scanner:")
print("Atual:", repr(scanner.atual))
print("Próximo:", repr(scanner.proximo))
print("Linha:", scanner.linha)

scanner.avancar()

print("\nApós primeiro avancar():")
print("Atual:", repr(scanner.atual))
print("Próximo:", repr(scanner.proximo))
print("Linha:", scanner.linha)

scanner.avancar()

print("\nApós segundo avancar():")
print("Atual:", repr(scanner.atual))
print("Próximo:", repr(scanner.proximo))
print("Linha:", scanner.linha)