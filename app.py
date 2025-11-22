import pandas as pd
import streamlit as st

st.write("Olá, Mundo dos Dados! 🚀")
st.write("Se você está lendo isso, o Streamlit funcionou.")
# Tente preencher aqui e me mostre:
dados = pd.read_csv("vendas.csv")
st.dataframe(dados)
# ... código anterior ...

st.title("Dashboard de Vendas 📊")

# Calcula o faturamento total (Soma da coluna 'Valor Total')
faturamento = dados['Valor Total'].sum()  # Dica: comando em inglês para somar é 'sum'

# Mostra o KPI grande na tela
st.metric("Faturamento Total", faturamento)

# ... st.dataframe(dados) fica aqui embaixo ...
st.write("---") # Uma linha divisória visual
st.subheader("Vendas no Tempo 📈")

# Preencha com 'Data' e 'Valor Total'
vendas_diarias = dados.groupby('Data')['Valor Total'].sum()

# Plota o gráfico de linha
st.line_chart(vendas_diarias)
st.write("---")
st.subheader("Top Produtos 🏆")

# Preencha com 'Produto' e 'Valor Total'
vendas_produtos = dados.groupby('Produto')['Valor Total'].sum()

# Plota o gráfico de barras (atenção ao comando: bar_chart)
st.bar_chart(vendas_produtos)
st.write("---")
st.subheader("Vendas por Filial 🏪")

# Crie a tabela agrupada por Filial
vendas_filiais = dados.groupby('Filial')['Valor Total'].sum()

# Crie o gráfico de barras
st.bar_chart(vendas_filiais)