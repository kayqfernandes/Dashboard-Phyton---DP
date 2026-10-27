#rodar codigo ./.venv/bin/python -m streamlit run painel.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
df = pd.read_excel("VULC3_evolucao.xlsx")

linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df[linhas][colunas]
fig, ax = plt.subplots()
sns.lineplot(dados, x= 'trimestre', y='valor',)
ax.set_title("Gráfico do lucro")

tab1, tab2= st.tabs(["Tab 1", "Tab 2"])

with tab1:
    st.title("SLA")
    st.pyplot(fig)
    st.dataframe(df)

with tab2:
    st.dataframe(df)

    df_size = df.groupby("categoria").size()

    fig, ax = plt.subplots()
    df_size.plot(kind="bar", ax=ax)

    ax.set_title("SLA2")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Quantidade")

    st.pyplot(fig)