import matplotlib.pyplot as plt
import numpy as np


with open("output/points.txt", "r") as arquivo:
    linhas = arquivo.readlines()
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
        plt.plot(x, y, marker='o', label=nome_classe)

plt.legend()
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title("Trajetória dos Objetos por Classe")
plt.grid()
plt.show()