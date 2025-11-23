import pandas as pd

# Lendo sem cabeçalho (header=None) para ver as primeiras linhas brutas
df_teste = pd.read_excel('CRM - BNI - EUA.xlsx', sheet_name='2025.10', header=None)

# Mostra as primeiras 15 linhas
print(df_teste.head(15))