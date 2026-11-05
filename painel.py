
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="VULC Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# IDENTIDADE VISUAL
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0B100D;
    --surface: #121A15;
    --surface2: #18231C;
    --border: #26362C;
    --green: #65E6A3;
    --text: #F0F5F1;
    --muted: #87998D;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background: #101812;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

h1, h2, h3 {
    color: var(--text) !important;
    letter-spacing: -1px;
}

p, label {
    color: var(--muted);
}

div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    transition: all .2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--green);
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 27px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface);
    border-color: var(--border);
    border-radius: 10px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

.stButton button, .stDownloadButton button {
    background: var(--green);
    color: #0B100D;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    transition: .2s;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #8AF0B9;
    color: #0B100D;
    border: none;
}

hr {
    border-color: var(--border);
}

[data-testid="stTabs"] button {
    font-weight: 600;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--green) !important;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

@st.cache_data
def carregar_dados():
    df = pd.read_excel("VULC3_evolucao.xlsx")

    df["valor"] = pd.to_numeric(
        df["valor"], errors="coerce"
    )

    df["conta"] = df["conta"].astype(str)
    df["trimestre"] = df["trimestre"].astype(str)

    return df


try:
    df = carregar_dados()

except Exception as e:
    st.error(f"Erro ao carregar a base de dados: {e}")
    st.stop()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 25px 0;">
        <div style="font-size:25px; font-weight:800;">
            <span style="color:#65E6A3;">◈</span>
            VULC
        </div>
        <div style="color:#87998D; font-size:11px; letter-spacing:2px;">
            ANALYTICS PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navegação")

    pagina = st.radio(
        "Menu",
        ["Visão geral", "Indicadores", "Base de dados"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Filtros")

    trimestres = sorted(df["trimestre"].dropna().unique())

    contas = sorted(df["conta"].dropna().unique())

    filtro_trimestre = st.multiselect(
        "Período",
        trimestres,
        default=trimestres
    )

    filtro_conta = st.multiselect(
        "Contas",
        contas,
        default=contas
    )

    st.divider()

    if st.button("↻ Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
    <div style="margin-top:40px; color:#718477; font-size:11px;">
        VULC ANALYTICS<br>
        Financial Intelligence
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# FILTRAGEM
# ==========================================

df_filtrado = df[
    df["trimestre"].isin(filtro_trimestre)
    & df["conta"].isin(filtro_conta)
].copy()

dados_lucro = df_filtrado[
    (df_filtrado["conta"].str.lower() == "lucro")
    & (df_filtrado["valor"].notna())
].copy()

total_registros = len(df_filtrado)

total_contas = df_filtrado["conta"].nunique()

lucro_total = dados_lucro["valor"].sum()

lucro_medio = (
    dados_lucro["valor"].mean()
    if not dados_lucro.empty else 0
)


# ==========================================
# FORMATAÇÃO
# ==========================================

def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================
# CABEÇALHO
# ==========================================

st.markdown("""
<div style="display:flex; justify-content:space-between;
align-items:center; flex-wrap:wrap;">

<div>
    <div style="color:#65E6A3; font-size:11px;
    font-weight:700; letter-spacing:2px;">
        FINANCIAL OVERVIEW
    </div>
    <h1 style="font-size:34px; margin:5px 0;">
        Painel de Indicadores
    </h1>
    <p style="color:#87998D; font-size:14px;">
        Acompanhe o desempenho financeiro da operação.
    </p>
</div>

<div style="background:#18231C; border:1px solid #26362C;
padding:10px 16px; border-radius:10px; color:#65E6A3;
font-size:12px;">
    ● DADOS CARREGADOS
</div>

</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# PÁGINA 1 - VISÃO GERAL
# ==========================================

if pagina == "Visão geral":

    st.markdown("### Indicadores principais")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Lucro acumulado",
            moeda(lucro_total)
        )

    with c2:
        st.metric(
            "Lucro médio",
            moeda(lucro_medio)
        )

    with c3:
        st.metric(
            "Total de registros",
            f"{total_registros:,}".replace(",", ".")
        )

    with c4:
        st.metric(
            "Contas cadastradas",
            total_contas
        )

    st.write("")

    # GRÁFICOS

    col1, col2 = st.columns([1.7, 1])

    with col1:

        st.markdown("### Evolução do lucro")

        if not dados_lucro.empty:

            lucro_trimestre = (
                dados_lucro
                .groupby("trimestre", as_index=False)["valor"]
                .sum()
            )

            fig = px.line(
                lucro_trimestre,
                x="trimestre",
                y="valor",
                markers=True
            )

            fig.update_traces(
                line=dict(color="#65E6A3", width=3),
                marker=dict(size=9, color="#65E6A3"),
                fill="tozeroy",
                fillcolor="rgba(101,230,163,0.08)",
                hovertemplate="<b>%{x}</b><br>Lucro: R$ %{y:,.2f}<extra></extra>"
            )

            fig.update_layout(
                template="plotly_dark",
                height=370,
                paper_bgcolor="#121A15",
                plot_bgcolor="#121A15",
                margin=dict(l=20, r=20, t=25, b=20),
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
                font=dict(family="Inter", color="#87998D"),
                hovermode="x unified"
            )

            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(
                gridcolor="#26362C",
                zeroline=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("Sem dados de lucro para o período.")

    with col2:

        st.markdown("### Distribuição por conta")

        distribuicao = (
            df_filtrado
            .groupby("conta")
            .size()
            .reset_index(name="quantidade")
        )

        if not distribuicao.empty:

            fig2 = px.pie(
                distribuicao,
                names="conta",
                values="quantidade",
                hole=0.72
            )

            fig2.update_layout(
                template="plotly_dark",
                height=370,
                paper_bgcolor="#121A15",
                plot_bgcolor="#121A15",
                margin=dict(l=10, r=10, t=25, b=10),
                legend=dict(
                    orientation="h",
                    y=-0.12,
                    font=dict(size=10)
                )
            )

            fig2.update_traces(
                textposition="inside",
                textinfo="percent",
                hole=0.72
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:
            st.info("Nenhum registro encontrado.")

    st.write("")
    st.markdown("### Últimos registros")

    st.dataframe(
        df_filtrado.tail(10),
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# PÁGINA 2 - INDICADORES
# ==========================================

elif pagina == "Indicadores":

    st.markdown("### Análise detalhada")

    if not df_filtrado.empty:

        resumo = (
            df_filtrado
            .groupby("conta")
            .agg(
                Quantidade=("valor", "count"),
                Total=("valor", "sum"),
                Média=("valor", "mean")
            )
            .reset_index()
        )

        resumo.columns = [
            "Conta",
            "Quantidade",
            "Total",
            "Média"
        ]

        resumo["Total"] = resumo["Total"].apply(moeda)
        resumo["Média"] = resumo["Média"].apply(moeda)

        st.dataframe(
            resumo,
            use_container_width=True,
            hide_index=True
        )

        st.write("")

        st.markdown("### Volume de registros por conta")

        fig = px.bar(
            resumo,
            x="Conta",
            y="Quantidade",
            text="Quantidade"
        )

        fig.update_traces(
            marker_color="#65E6A3",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400,
            paper_bgcolor="#121A15",
            plot_bgcolor="#121A15",
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )

        fig.update_yaxes(gridcolor="#26362C")
        fig.update_xaxes(showgrid=False)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("Não existem dados para os filtros selecionados.")


# ==========================================
# PÁGINA 3 - BASE DE DADOS
# ==========================================

elif pagina == "Base de dados":

    st.markdown("### Exploração de dados")

    pesquisa = st.text_input(
        "⌕ Pesquisar na base",
        placeholder="Digite uma conta ou trimestre..."
    )

    dados_tabela = df_filtrado.copy()

    if pesquisa:

        mascara = dados_tabela.astype(str).apply(
            lambda coluna: coluna.str.contains(
                pesquisa,
                case=False,
                na=False
            )
        ).any(axis=1)

        dados_tabela = dados_tabela[mascara]

    st.markdown(
        f"**{len(dados_tabela)} registros encontrados**"
    )

    st.dataframe(
        dados_tabela,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.download_button(
        "↓ Exportar dados em CSV",
        data=dados_tabela.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="vulc_dados.csv",
        mime="text/csv"
    )


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.markdown("""
<div style="display:flex; justify-content:space-between;
flex-wrap:wrap; color:#718477; font-size:11px;">

<span>VULC ANALYTICS · FINANCIAL INTELLIGENCE</span>
<span>Desenvolvido com Streamlit</span>

</div>
""", unsafe_allow_html=True)
