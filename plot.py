import matplotlib.pyplot as plt
import numpy as np


with open("points.txt", "r") as arquivo:
    linhas = arquivo.readlines()
# Separando o cabeçalho (nomes das classes)
nomes_classes = linhas[0].strip().split("\t")  
# Criando dicionário vazio para armazenar os pontos de cada classe
pontos = {classe: [] for classe in nomes_classes}
# Processando as linhas do arquivo (ignorando o cabeçalho)
for linha in linhas[1:]:
    valores = linha.strip().split("\t")  
    for i, valor in enumerate(valores):
        if valor: 
            valor = valor.replace("(", "").replace(")", "").split(", ")  
            x = float(valor[0])  
            y = float(valor[1])
            pontos[nomes_classes[i]].append((x, y)) 

# Plotando os pontos
plt.figure(figsize=(8, 6))
for nome_classe, pontos_classe in pontos.items():
    if pontos_classe:  
        x = [p[0] for p in pontos_classe]
        y = [p[1] for p in pontos_classe]
        plt.plot(x, y, marker='o', linestyle='-', label=nome_classe)

plt.legend()
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title("Trajetória dos Objetos por Classe")
plt.grid()
plt.show()




#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# import matplotlib.pyplot as plt
# import numpy as np

# # Lendo o arquivo txt
# with open("points.txt", "r") as arquivo:
#     linhas = arquivo.readlines()

# # Separando o cabeçalho (nomes das classes)
# nomes_classes = linhas[0].strip().split("\t")  # Primeira linha contém os nomes das classes

# # Criando dicionário vazio para armazenar os pontos de cada classe
# pontos = {classe: [] for classe in nomes_classes}

# # Processando as linhas do arquivo (ignorando o cabeçalho)
# for linha in linhas[1:]:
#     valores = linha.strip().split("\t")  # Separando os valores por tabulação

#     # Iterando sobre cada classe e seu respectivo valor de ponto
#     for i, valor in enumerate(valores):
#         if valor:  # Ignora valores vazios
#             valor = valor.replace("(", "").replace(")", "").split(", ")  # Remove parênteses e separa x, y
#             x = float(valor[0])  # Convertendo para float
#             y = float(valor[1])
#             pontos[nomes_classes[i]].append((x, y))  # Adiciona ao dicionário na classe correspondente

# # Solicitando o nome da classe a ser plotada
# nome_entrada = input(f"Digite o nome da classe para plotar ({', '.join(nomes_classes)}): ")

# # Verificando se a classe está no dicionário
# if nome_entrada in pontos and pontos[nome_entrada]:
#     # Pegando os pontos da classe escolhida
#     x = [p[0] for p in pontos[nome_entrada]]
#     y = [p[1] for p in pontos[nome_entrada]]

#     # Plotando apenas a classe selecionada
#     plt.figure(figsize=(8, 6))
#     plt.plot(x, y, marker='o', linestyle='-', label=nome_entrada)
#     plt.legend()
#     plt.xlabel("Coordenada X")
#     plt.ylabel("Coordenada Y")
#     plt.title(f"Trajetória da Classe: {nome_entrada}")
#     plt.grid()
#     plt.show()
# else:
#     print(f"Classe '{nome_entrada}' não encontrada ou sem pontos disponíveis.")
