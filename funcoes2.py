# Funções, em Python, são para organizar sequencias de comandos.
# A sua principal finalidade é nos ajudar a organizar programas em pedaços que correspondam a como imaginamos uma solução do problema

def minha_funcao(argumento_entrada):
    pass #corpo da função

# Argumento de entrada = pode ser qualquer valor válido em python e em qualquer quntidade de itens
# Corpo da função = onde se organiza as tarefas
# Pode-se, também, retornar valores

def login(a, b):
    senha = input("Digite a Senha\n")

    if senha == '1234':
        print("Senha correta")
    else:
        print("Senha incorreta, favor tentar novamente.")

print("Entrou no programa")
login(2,2)
print("Saiu do programa")
