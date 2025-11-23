import pandas as pd
import streamlit as st
import plotly.express as px
import os

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard SDR", layout="wide")

# --- CONFIGURAÇÃO DO ARQUIVO ---
# 👇 COLE O CAMINHO AQUI (Mantenha o r e as aspas)
arquivo = r"E:\Download\CRM - BNI - EUA.xlsx"

# 2. Carregamento de Dados (Blindado)
@st.cache_data
def carregar_dados():
    if not os.path.exists(arquivo):
        return None
    
    try:
        # Lê as abas de Out e Nov (Título na linha 6 = header 5)
        df_out = pd.read_excel(arquivo, sheet_name='2025.10', header=5)
        df_nov = pd.read_excel(arquivo, sheet_name='2025.11', header=5)
        
        # Junta tudo
        df = pd.concat([df_out, df_nov])
        
        # Tratamento simples: Preenche vazios da coluna Status
        if 'Status' in df.columns:
            df['Status'] = df['Status'].fillna('Sem Retorno')
            
        return df
    except Exception as e:
        st.error(f"Erro na leitura: {e}")
        return pd.DataFrame()

# 3. Construção do Painel
df = carregar_dados()

if df is None:
    st.error("🚫 ARQUIVO NÃO ENCONTRADO!")
    st.info("Vá na linha 10 do código e cole o caminho do arquivo (copie com Shift+Botão Direito).")

elif not df.empty:
    st.title("📊 Monitoramento de Prospecção")
    st.markdown("---")

    # Verifica se as colunas essenciais existem
    colunas_ok = True
    if 'SDR' not in df.columns:
        st.error("Erro: Não achei a coluna 'SDR'.")
        colunas_ok = False
    if 'Status' not in df.columns:
        st.error("Erro: Não achei a coluna 'Status'.")
        colunas_ok = False

    if colunas_ok:
        # Cria as duas abas que você pediu
        tab1, tab2 = st.tabs(["🏆 Ranking SDR", "🌪️ Status Geral"])

        # ABA 1: QUEM FEZ MAIS?
        with tab1:
            st.subheader("Volume por SDR")
            # Conta e cria o gráfico
            ranking = df['SDR'].value_counts().reset_index()
            ranking.columns = ['SDR', 'Quantidade']
            
            fig = px.bar(ranking, x='SDR', y='Quantidade', color='SDR', text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

        # ABA 2: COMO ESTÃO AS PROSPECÇÕES?
        with tab2:
            st.subheader("Distribuição dos Status")
            # Conta e cria o gráfico
            status_geral = df['Status'].value_counts().reset_index()
            status_geral.columns = ['Status', 'Quantidade']
            
            fig2 = px.pie(status_geral, values='Quantidade', names='Status', hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Mostra a tabela também
            st.dataframe(status_geral, hide_index=True)