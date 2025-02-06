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
        plt.scatter(x, y, marker='o', label=nome_classe)

plt.legend()
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title("Trajetória dos Objetos por Classe")
plt.grid()
plt.show()


#################################################################
# valores positivos (em caso de falha na detecção)
with open("output/points.txt", "r") as arquivo:
    linhas = arquivo.readlines()

nomes_classes = linhas[0].strip().split("\t")  
pontos = {classe: [] for classe in nomes_classes if classe != "Field"}  

for linha in linhas[1:]:
    valores = linha.strip().split("\t")  
    for i, valor in enumerate(valores):
        if nomes_classes[i] != "Field" and valor:  
            valor = valor.replace("(", "").replace(")", "").split(", ")  
            x, y = float(valor[0]), float(valor[1])

            if x >= 0 and y >= 0:  # Filtrar valores negativos
                pontos[nomes_classes[i]].append((x, y))  

plt.figure(figsize=(8, 6))
for nome_classe, pontos_classe in pontos.items():
    if pontos_classe:  
        x = [p[0] for p in pontos_classe]
        y = [p[1] for p in pontos_classe]
        plt.scatter(x, y, marker='o', label=nome_classe)

plt.legend()
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title("Trajetória dos Objetos por Classe")
plt.grid()
plt.show()


#########################################################################
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados do arquivo points.txt
with open("output/points.txt", "r") as arquivo:
    linhas = arquivo.readlines()

# Ler os nomes das classes
nomes_classes = linhas[0].strip().split("\t")
classes_desejadas = ["Ball", "Yellow Robot", "Blue Robot"]

# Criar dicionário para armazenar os pontos
pontos = {classe: [] for classe in nomes_classes if classe in classes_desejadas}

# Processar as linhas do arquivo
for linha in linhas[1:]:
    valores = linha.strip().split("\t")
    for i, valor in enumerate(valores):
        if nomes_classes[i] in classes_desejadas and valor:
            valor = valor.replace("(", "").replace(")", "").split(", ")
            x = float(valor[0])
            y = float(valor[1])
            if x >= 0 and y >= 0:  # Excluir linhas com valores negativos
                pontos[nomes_classes[i]].append((x, y))

# Criar subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

cores = {"Ball": "orange", "Yellow Robot": "yellow", "Blue Robot": "blue"}
estilos = {"Ball": "-", "Yellow Robot": "--", "Blue Robot": "-"}

# Plotando X ao longo do tempo para cada classe
for classe, pontos_classe in pontos.items():
    if pontos_classe:
        tempo = np.arange(len(pontos_classe))  # Criar vetor de tempo baseado no número de pontos da classe
        x_vals = [p[0] for p in pontos_classe]
        axs[0].plot(tempo, x_vals, label=classe, color=cores[classe], linestyle=estilos[classe])

axs[0].set_ylabel(r"$x (mm)$", fontsize=12, fontstyle='italic')
axs[0].legend()
axs[0].grid()

# Plotando Y ao longo do tempo para cada classe
for classe, pontos_classe in pontos.items():
    if pontos_classe:
        tempo = np.arange(len(pontos_classe))  # Criar vetor de tempo baseado no número de pontos da classe
        y_vals = [p[1] for p in pontos_classe]
        axs[1].plot(tempo, y_vals, label=classe, color=cores[classe], linestyle=estilos[classe])

axs[1].set_xlabel(r"$time (frames)$", fontsize=12, fontstyle='italic')
axs[1].set_ylabel(r"$y (mm)$", fontsize=12, fontstyle='italic')
axs[1].grid()

plt.tight_layout()
plt.show()