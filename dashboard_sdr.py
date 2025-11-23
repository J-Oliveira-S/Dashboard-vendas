import pandas as pd
import streamlit as st
import plotly.express as px
import os
import bcrypt # NOVO: Biblioteca para checagem segura de hash 
# --- CÓDIGO DE DIAGNÓSTICO TEMPORÁRIO (DEPOIS APAGUE) ---
# st.error("DEBUG HASH: Verifique o hash que está sendo lido:")
# st.code(st.secrets.credentials.passwords[0])
# --- FIM DO CÓDIGO DE DIAGNÓSTICO ---
# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Dashboard SDR - ITECA", layout="wide")

# ⚠️ Linha 15: COLE O CAMINHO ABSOLUTO DO SEU ARQUIVO AQUI ⚠️
arquivo = r"E:\Download\CRM - BNI - EUA.xlsx"

# --- 2. FUNÇÃO DE CARREGAMENTO (ETL) ---
@st.cache_data
def carregar_dados(file_path):
    print(f"Conteúdo de file_path: {file_path}")
    print(f"Tipo de file_path: {type(file_path)}")
    if not os.path.exists(file_path):
        return None, None
    try:
        df_out = pd.read_excel(file_path, sheet_name='2025.10', header=5)
        df_nov = pd.read_excel(file_path, sheet_name='2025.11', header=5)
        df_vars = pd.read_excel(file_path, sheet_name='Variables')
        df_out['Mês'] = 'Outubro'; df_nov['Mês'] = 'Novembro'
        df_total = pd.concat([df_out, df_nov])
        df_total['Status'] = df_total['Status'].fillna('Sem Retorno')
        df_total['Contact'] = pd.to_datetime(df_total['Contact'], errors='coerce')
        df_total['Semana'] = df_total['Contact'].dt.strftime('%Y-%U')
        return df_total, df_vars
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()


# --- 3. LÓGICA DE AUTENTICAÇÃO SEGURA (NATIVA) ---

# Função para checar a senha contra o HASH seguro no secrets.toml
def check_password_native(password):
    # A senha está armazenada em bytes no secrets.toml
    hashed_pass_bytes = st.secrets.credentials.passwords[0].encode()
    return bcrypt.checkpw(password.encode(), hashed_pass_bytes)

# Inicializa o estado de autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- TELA DE LOGIN ---
if not st.session_state['authenticated']:
    st.title('🔒 Login ITECA')
    
    with st.form("Login"):
        # Campo de usuário (fácil, pois só temos um)
        username = st.text_input('Usuário:', value=st.secrets.credentials.usernames[0], disabled=True)
        # Campo de senha (Tipo 'password' deixa a senha invisível)
        password = st.text_input('Senha:', type='password', key='password_input')
        
        submitted = st.form_submit_button('Entrar')

        if submitted:
            if check_password_native(password):
                st.session_state['authenticated'] = True
                st.rerun() # Reinicia para carregar o dashboard
            else:
                st.error('Senha incorreta. Tente novamente.')

# --- 4. CONTEÚDO PRINCIPAL DO DASHBOARD (Aberto após o Login) ---
if st.session_state['authenticated']:
    # Chamada de dados e lógica principal
    st.sidebar.title(f"Bem-vindo(a), {st.secrets.credentials.names[0].split()[0]}!")
    
    # Botão de Logout
    if st.sidebar.button("Sair"):
        st.session_state['authenticated'] = False
        st.rerun()

    # --- Carrega dados APENAS SE AUTENTICADO ---
    df, df_variaveis = carregar_dados(arquivo) 

    if df is None:
        st.error("🚫 ARQUIVO NÃO ENCONTRADO! Verifique o caminho na linha 15.")
    
    elif not df.empty:
        st.title(f"🚀 Dashboard de Performance SDR")
        # ... (O restante do seu código segue aqui) ...
        
        # O BLOCO ABAIXO CONTÉM TODOS OS GRÁFICOS (mantido alinhado)
        
        # --- KPIs DO TOPO ---
        total = len(df); agendados = df[df['Status'].isin(['Call Done', 'No show', '1v1'])].shape[0]
        realizados = df[df['Status'] == 'Call Done'].shape[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Prospectado", total)
        c2.metric("Agendamentos", agendados)
        c3.metric("Realizados", realizados)
        if total > 0: c4.metric("Conversão Global", f"{(agendados/total)*100:.1f}%")

        st.divider()

        # --- ABAS DE ANÁLISE ---
        tab1, tab2, tab3, tab4 = st.tabs(["🏆 Ranking SDR", "💼 Profissões", "📊 Variables", "🌪️ Funil"])

        # ABA 1: RANKING SDR
        with tab1:
            if 'SDR' in df.columns:
                st.subheader("Volume por SDR")
                ranking = df['SDR'].value_counts().reset_index()
                ranking.columns = ['SDR', 'Leads']
                fig_rank = px.bar(ranking, x='SDR', y='Leads', color='SDR', text_auto=True)
                st.plotly_chart(fig_rank, use_container_width=True)

        # ABA 2: PROFISSÕES (Mapa de Calor)
        with tab2:
            st.subheader("Análise de Qualidade por Nicho")
            if 'Profession' in df.columns and 'Status' in df.columns:
                df_prof = df.groupby('Profession').agg(Total=('Status', 'count'), Interacoes=('Status', lambda x: x[x != 'Sem Retorno'].count())).reset_index()
                df_prof['Taxa (%)'] = (df_prof['Interacoes'] / df_prof['Total']) * 100
                top_prof = df_prof.sort_values(by='Total', ascending=False).head(15).sort_values(by='Total', ascending=True)
                fig_prof = px.bar(top_prof, x='Total', y='Profession', orientation='h', color='Taxa (%)', color_continuous_scale='RdYlGn', title="Top 15 Profissões")
                st.plotly_chart(fig_prof, use_container_width=True)

        # ABA 3: VARIABLES (Metas)
        with tab3:
            st.subheader("Evolução Semanal e Metas")
            if not df_variaveis.empty:
                c_var1, c_var2 = st.columns(2)
                with c_var1:
                    fig_sc = px.scatter(df_variaveis, x="Outreachs", y="Scheduled 1:1", color="Month", title="Esforço vs. Agendamento")
                    st.plotly_chart(fig_sc, use_container_width=True)
                with c_var2:
                    fig_ln = px.line(df_variaveis, x="Week", y="Scheduling rate", markers=True, title="Taxa de Conversão Semanal")
                    st.plotly_chart(fig_ln, use_container_width=True)
            else: st.info("A aba 'Variables' não foi carregada.")

        # ABA 4: FUNIL
        with tab4:
            st.subheader("Funil de Eficiência")
            funil_df = pd.DataFrame({'Etapa': ['Prospecção', 'Agendamento', 'Realização'], 'Valor': [total, agendados, realizados]})
            st.plotly_chart(px.funnel(funil_df, x='Valor', y='Etapa'), use_container_width=True)
            
    # --- TRATAMENTO DE ERROS DE DADOS ---
    elif df is None:
        st.error(f"🚫 ARQUIVO NÃO ENCONTRADO! Verifique o caminho na linha 15.")
    
    else:
        st.warning("O arquivo foi encontrado, mas a base de dados está vazia.")