import pandas as pd
import random
from datetime import datetime, timedelta

# Configurações
linhas = 1000 # Vamos criar 1000 vendas!
produtos = [
    ('Notebook', 5000.00, 'Eletrônicos'),
    ('Joystick', 450.00, 'Acessório'),
    ('Mouse Gamer', 200.00, 'Acessórios'),
    ('Teclado Mecânico', 450.00, 'Acessórios'),
    ('Monitor 24"', 1200.00, 'Eletrônicos'),
    ('Cadeira Ergonômica', 800.00, 'Móveis'),
    ('Headset', 300.00, 'Acessórios')
]
filiais = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 'Recife']

dados = []

# O Loop (Repetição)
for _ in range(linhas):
    prod, preco, cat = random.choice(produtos)
    data_venda = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
    
    venda = {
        'Data': data_venda,
        'Produto': prod,
        'Categoria': cat,
        'Preço Unitário': preco,
        'Quantidade': random.randint(1, 5),
        'Filial': random.choice(filiais)
    }
    # Calcula o valor total daquela venda
    venda['Valor Total'] = venda['Preço Unitário'] * venda['Quantidade']
    dados.append(venda)

# Transforma em tabela (DataFrame) e salva
df = pd.DataFrame(dados)
df.to_csv('vendas.csv', index=False)

print("Arquivo 'vendas.csv' criado com sucesso com 1000 vendas!")