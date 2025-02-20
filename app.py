import streamlit as st
import pandas as pd

# Definir estilo global com fundo branco e títulos azul escuro
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        h1, h2 {
            color: #003366;
        }
        .stDataFrame, .stTable {
            background-color: white;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho do Dashboard
st.markdown("<h1 style='text-align: center; color: #003366;'>Dashboard de Movimentação Portuária - Maranhão</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "dados_graficos.xlsx"
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        'Ano': 'ano',
        'Tipo de instalação': 'tipo_instalacao',
        'Perfil da Carga': 'perfil_carga',
        'Sentido': 'sentido',
        'Tipo Navegação': 'tipo_navegacao',
        'UF Origem': 'uf_origem',
        'UF Destino': 'uf_destino',
        'País Origem': 'pais_origem',
        'País Destino': 'pais_destino',
        'Total de Movimentação Portuária\nem toneladas (t)': 'movimentacao_total_t'
    })
    df["ano"] = df["ano"].astype(int).astype(str)  # Garantir formato correto de ano
    
    # Filtrar apenas os dados do Maranhão (MA)
    df = df[(df["uf_origem"] == "MA") | (df["uf_destino"] == "MA")]
    return df

df = load_data()

# Filtros ampliados
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()), index=0)
tipo_instalacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Instalação", ["Todos"] + list(df["tipo_instalacao"].unique()), index=0)
perfil_carga_selecionado = st.sidebar.selectbox("Selecione o Perfil da Carga", ["Todos"] + list(df["perfil_carga"].unique()), index=0)
sentido_selecionado = st.sidebar.selectbox("Selecione o Sentido", ["Todos"] + list(df["sentido"].unique()), index=0)
tipo_navegacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Navegação", ["Todos"] + list(df["tipo_navegacao"].unique()), index=0)

# Aplicar filtros
df_filtered = df[df["ano"] == ano_selecionado]
if tipo_instalacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_instalacao"] == tipo_instalacao_selecionado]
if perfil_carga_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["perfil_carga"] == perfil_carga_selecionado]
if sentido_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["sentido"] == sentido_selecionado]
if tipo_navegacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_navegacao"] == tipo_navegacao_selecionado]

# Agregar dados por ano
df_summary = df_filtered.groupby("ano", as_index=False)["movimentacao_total_t"].sum()

# Formatar os números para exibição
df_summary["movimentacao_total_t"] = df_summary["movimentacao_total_t"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Exibir tabela de dados agregados
st.dataframe(df_summary, width=1000)

# Crédito 
st.write("Fonte: Estatístico Aquaviário ANTAQ")
st.markdown("<p><strong>Ferramenta desenvolvida por Darliane Cunha.</strong></p>", unsafe_allow_html=True)
