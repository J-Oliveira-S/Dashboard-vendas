import sys
import os

print("--- RELATÓRIO DO ESPIÃO ---")
print(f"1. Eu sou o Python que mora aqui:\n{sys.executable}")
print("-" * 30)

try:
    import plotly
    print(f"2. SUCESSO! Encontrei o Plotly aqui:\n{os.path.dirname(plotly.__file__)}")
except ImportError:
    print("2. FRACASSO: Não encontrei o Plotly neste ambiente.")
    print("   (Precisamos instalar especificamente para o Python listado acima)")