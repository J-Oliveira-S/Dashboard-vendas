import os

# 1. Onde o Python acha que está?
print("Estou rodando nesta pasta:", os.getcwd())

# 2. O que o Python vê aqui dentro?
print("\nArquivos que eu consigo ver:")
for arquivo in os.listdir():
    print(f"- '{arquivo}'")