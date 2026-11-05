import html

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="VULC Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# IDENTIDADE VISUAL
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0B100D;
        --surface: #121A15;
        --surface-2: #18231C;
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

    /* Cards KPI personalizados: sem corte e sem reticências */
    .kpi-card {
        box-sizing: border-box;
        width: 100%;
        min-width: 0;
        min-height: 142px;
        padding: 21px 20px 18px 20px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 15px;
        transition: border-color .2s ease, transform .2s ease;
        overflow: visible;
    }

    .kpi-card:hover {
        border-color: var(--green);
        transform: translateY(-2px);
    }

    .kpi-label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 500;
        line-height: 1.4;
        margin-bottom: 13px;
    }

    .kpi-value {
        display: block;
        width: 100%;
        color: var(--text);
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -1.1px;
        white-space: nowrap;
        overflow: visible;
        text-overflow: clip;
        font-variant-numeric: tabular-nums;
    }

    .kpi-note {
        margin-top: 10px;
        color: #718477;
        font-size: 11px;
        line-height: 1.3;
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

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 900px) {
        .kpi-card {
            min-height: 128px;
            padding: 17px 15px;
        }
        .kpi-label {
            font-size: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNÇÕES DE FORMATAÇÃO
# =========================================================
def moeda(valor, casas=2):
    """Formata valores no padrão brasileiro: R$ 1.234.567,89."""
    if pd.isna(valor):
        return "—"
    numero = f"{float(valor):,.{casas}f}"
    numero = numero.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {numero}"


def numero_br(valor, casas=2):
    """Formata número no padrão brasileiro, sem símbolo monetário."""
    if pd.isna(valor):
        return "—"
    numero = f"{float(valor):,.{casas}f}"
    return numero.replace(",", "X").replace(".", ",").replace("X", ".")


def tamanho_fonte_kpi(texto):
    """Reduz a fonte de valores longos para caber no card sem ocultar dígitos."""
    quantidade = len(str(texto))
    return max(15, min(25, 390 / max(quantidade, 1)))


def mostrar_kpi(coluna, titulo, valor, observacao):
    valor_seguro = html.escape(str(valor))
    titulo_seguro = html.escape(str(titulo))
    observacao_segura = html.escape(str(observacao))
    fonte = tamanho_fonte_kpi(str(valor))

    with coluna:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{titulo_seguro}</div>
                <div class="kpi-value" style="font-size:{fonte:.1f}px;">{valor_seguro}</div>
                <div class="kpi-note">{observacao_segura}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def formatar_tabela(dados):
    """Prepara uma cópia visual da tabela sem alterar os dados originais."""
    visual = dados.copy()
    if "valor" in visual.columns:
        visual["valor"] = visual["valor"].apply(moeda)
    return visual


# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================
@st.cache_data

def carregar_dados():
    df = pd.read_excel("VULC3_evolucao.xlsx")

    colunas_necessarias = {"valor", "conta", "trimestre"}
    faltantes = colunas_necessarias.difference(df.columns)
    if faltantes:
        raise ValueError(
            "A planilha não contém as colunas necessárias: "
            + ", ".join(sorted(faltantes))
        )

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["conta"] = df["conta"].fillna("Sem classificação").astype(str)
    df["trimestre"] = df["trimestre"].fillna("Sem período").astype(str)

    return df


try:
    df = carregar_dados()
except Exception as erro:
    st.error(f"Não foi possível carregar VULC3_evolucao.xlsx: {erro}")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding:12px 0 25px 0;">
            <div style="font-size:25px;font-weight:800;">
                <span style="color:#65E6A3;">◈</span> VULC
            </div>
            <div style="color:#87998D;font-size:11px;letter-spacing:2px;">
                ANALYTICS PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navegação")
    pagina = st.radio(
        "Menu",
        ["Visão geral", "Indicadores", "Base de dados"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Filtros")

    trimestres = sorted(df["trimestre"].dropna().unique().tolist())
    contas = sorted(df["conta"].dropna().unique().tolist())

    filtro_trimestre = st.multiselect(
        "Período", trimestres, default=trimestres
    )
    filtro_conta = st.multiselect(
        "Contas", contas, default=contas
    )

    st.divider()
    if st.button("↻ Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(
        """
        <div style="margin-top:40px;color:#718477;font-size:11px;">
            VULC ANALYTICS<br>Financial Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FILTRAGEM E INDICADORES
# =========================================================
df_filtrado = df[
    df["trimestre"].isin(filtro_trimestre)
    & df["conta"].isin(filtro_conta)
].copy()

dados_lucro = df_filtrado[
    (df_filtrado["conta"].str.strip().str.lower() == "lucro")
    & df_filtrado["valor"].notna()
].copy()

total_registros = len(df_filtrado)
total_contas = df_filtrado["conta"].nunique()
lucro_total = dados_lucro["valor"].sum()
lucro_medio = dados_lucro["valor"].mean() if not dados_lucro.empty else 0


# =========================================================
# CABEÇALHO
# =========================================================
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
            <div style="color:#65E6A3;font-size:11px;font-weight:700;letter-spacing:2px;">
                FINANCIAL OVERVIEW
            </div>
            <h1 style="font-size:34px;margin:5px 0;">Painel de Indicadores</h1>
            <p style="color:#87998D;font-size:14px;margin:0;">
                Acompanhe o desempenho financeiro da operação.
            </p>
        </div>
        <div style="background:#18231C;border:1px solid #26362C;padding:10px 16px;border-radius:10px;color:#65E6A3;font-size:12px;">
            ● DADOS CARREGADOS
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()


# =========================================================
# PÁGINA 1 — VISÃO GERAL
# =========================================================
if pagina == "Visão geral":
    st.markdown("### Indicadores principais")

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    mostrar_kpi(c1, "Lucro acumulado", moeda(lucro_total), "Soma do lucro no período selecionado")
    mostrar_kpi(c2, "Lucro médio", moeda(lucro_medio), "Média dos registros de lucro")
    mostrar_kpi(c3, "Total de registros", f"{total_registros:,}".replace(",", "."), "Registros após aplicação dos filtros")
    mostrar_kpi(c4, "Contas cadastradas", str(total_contas), "Contas presentes no período selecionado")

    st.write("")
    col1, col2 = st.columns([1.7, 1], gap="large")

    with col1:
        st.markdown("### Evolução do lucro")

        if not dados_lucro.empty:
            lucro_trimestre = (
                dados_lucro.groupby("trimestre", as_index=False)["valor"]
                .sum()
                .sort_values("trimestre")
            )

            fig = px.line(
                lucro_trimestre,
                x="trimestre",
                y="valor",
                markers=True,
            )
            fig.update_traces(
                line=dict(color="#65E6A3", width=3),
                marker=dict(size=9, color="#65E6A3", line=dict(width=1, color="#0B100D")),
                fill="tozeroy",
                fillcolor="rgba(101,230,163,0.08)",
                customdata=np.array(
                    [moeda(v) for v in lucro_trimestre["valor"]], dtype=object
                ).reshape(-1, 1),
                hovertemplate="<b>%{x}</b><br>Lucro: %{customdata[0]}<extra></extra>",
            )

            # Cinco marcações explícitas impedem o Plotly de abreviar em K/M.
            minimo = float(lucro_trimestre["valor"].min())
            maximo = float(lucro_trimestre["valor"].max())
            if minimo == maximo:
                margem = max(abs(minimo) * 0.01, 1)
                eixo_min, eixo_max = minimo - margem, maximo + margem
            else:
                margem = (maximo - minimo) * 0.12
                eixo_min, eixo_max = minimo - margem, maximo + margem

            marcas = np.linspace(eixo_min, eixo_max, 5)
            textos_marcas = [moeda(v) for v in marcas]

            fig.update_layout(
                template="plotly_dark",
                height=390,
                paper_bgcolor="#121A15",
                plot_bgcolor="#121A15",
                margin=dict(l=145, r=22, t=25, b=35),
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
                font=dict(family="Inter", color="#87998D"),
                hovermode="x unified",
            )
            fig.update_xaxes(showgrid=False, tickfont=dict(size=11))
            fig.update_yaxes(
                tickmode="array",
                tickvals=marcas,
                ticktext=textos_marcas,
                gridcolor="#26362C",
                zeroline=False,
                range=[eixo_min, eixo_max],
                tickfont=dict(size=10),
            )

            st.plotly_chart(fig, use_container_width=True)
            st.caption("Valores exibidos integralmente em reais. A escala vertical acompanha a variação dos dados.")
        else:
            st.info("Não existem dados de lucro para os filtros selecionados.")

    with col2:
        st.markdown("### Distribuição por conta")
        distribuicao = (
            df_filtrado.groupby("conta").size().reset_index(name="quantidade")
        )

        if not distribuicao.empty:
            paleta = ["#65E6A3", "#42C98B", "#2E9F70", "#A4E6BF", "#D0B36B", "#648F78", "#9A8CDB"]
            fig2 = px.pie(
                distribuicao,
                names="conta",
                values="quantidade",
                hole=0.70,
                color_discrete_sequence=paleta,
            )
            fig2.update_layout(
                template="plotly_dark",
                height=390,
                paper_bgcolor="#121A15",
                plot_bgcolor="#121A15",
                margin=dict(l=10, r=10, t=25, b=30),
                legend=dict(
                    orientation="h",
                    y=-0.12,
                    font=dict(size=10),
                ),
            )
            fig2.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont=dict(size=11),
                marker=dict(line=dict(color="#121A15", width=2)),
                hole=0.70,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado para os filtros selecionados.")

    st.write("")
    st.markdown("### Últimos registros")
    st.dataframe(
        formatar_tabela(df_filtrado.tail(10)),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# PÁGINA 2 — INDICADORES
# =========================================================
elif pagina == "Indicadores":
    st.markdown("### Análise detalhada")

    if not df_filtrado.empty:
        resumo = (
            df_filtrado.groupby("conta")
            .agg(
                Quantidade=("valor", "count"),
                Total=("valor", "sum"),
                Média=("valor", "mean"),
            )
            .reset_index()
        )
        resumo.columns = ["Conta", "Quantidade", "Total", "Média"]

        resumo_visual = resumo.copy()
        resumo_visual["Total"] = resumo_visual["Total"].apply(moeda)
        resumo_visual["Média"] = resumo_visual["Média"].apply(moeda)

        st.dataframe(
            resumo_visual,
            use_container_width=True,
            hide_index=True,
        )

        st.write("")
        st.markdown("### Volume de registros por conta")

        fig = px.bar(
            resumo,
            x="Conta",
            y="Quantidade",
            text="Quantidade",
            color_discrete_sequence=["#65E6A3"],
        )
        fig.update_traces(
            marker_color="#65E6A3",
            textposition="outside",
            cliponaxis=False,
        )
        fig.update_layout(
            template="plotly_dark",
            height=420,
            paper_bgcolor="#121A15",
            plot_bgcolor="#121A15",
            margin=dict(l=25, r=25, t=35, b=25),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            font=dict(family="Inter", color="#87998D"),
        )
        fig.update_yaxes(gridcolor="#26362C", rangemode="tozero")
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não existem dados para os filtros selecionados.")


# =========================================================
# PÁGINA 3 — BASE DE DADOS
# =========================================================
elif pagina == "Base de dados":
    st.markdown("### Exploração de dados")

    pesquisa = st.text_input(
        "⌕ Pesquisar na base",
        placeholder="Digite uma conta ou trimestre...",
    )

    dados_tabela = df_filtrado.copy()
    if pesquisa:
        mascara = dados_tabela.astype(str).apply(
            lambda coluna: coluna.str.contains(
                pesquisa,
                case=False,
                na=False,
                regex=False,
            )
        ).any(axis=1)
        dados_tabela = dados_tabela[mascara]

    st.markdown(f"**{len(dados_tabela):,} registros encontrados**".replace(",", "."))
    st.dataframe(
        formatar_tabela(dados_tabela),
        use_container_width=True,
        hide_index=True,
        height=520,
    )

    st.download_button(
        "↓ Exportar dados em CSV",
        data=dados_tabela.to_csv(index=False).encode("utf-8-sig"),
        file_name="vulc_dados.csv",
        mime="text/csv",
    )


# =========================================================
# RODAPÉ
# =========================================================
st.divider()
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;color:#718477;font-size:11px;">
        <span>VULC ANALYTICS · FINANCIAL INTELLIGENCE</span>
        <span>Desenvolvido com Streamlit</span>
    </div>
    """,
    unsafe_allow_html=True,
)
