# Condicionais, em Python, são estruturas usadas para tomar decisões

senha = ''

# operadores lógicos
# Comparação:
# ==  Igual a - Verifica se um valor é igual ao outro
# !=  Diferente de - Verifica se um valor é diferente ao outro
#  >  Maior que - Verifica se um valor é maior que outro
# >=  Maior ou igual - Verifica se um valor é maior ou igual ao outro
#  <  Menor que - Verifica se um valor é menor que outro
# <=  Menor ou igual - Verifica se um valor é menor ou igual ao outro

while senha != 'q':
    
    senha = input("Digite a Senha\n")

    if senha == '1234':
        print("Senha correta")
    else:
        print("Senha incorreta, favor tentar novamente.")
        
    senha = input("'c' - Continuar.\n'q' - Sair do Programa.\n")
        
    
