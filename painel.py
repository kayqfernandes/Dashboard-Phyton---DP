
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_excel("VULC3_evolucao.xlsx")

# Gráfico da evolução do lucro
linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df.loc[linhas, colunas]

fig1, ax1 = plt.subplots()
sns.lineplot(data=dados, x="trimestre", y="valor", ax=ax1)
ax1.set_title("Gráfico do lucro")

tab1, tab2 = st.tabs(["Page One", "Page Two"])

with tab1:
    st.title("SLA")
    st.pyplot(fig1)
    st.dataframe(df)

with tab2:
    st.dataframe(df)

    # Contagem de registros por conta
    df_size = df.groupby("conta").size()

    fig2, ax2 = plt.subplots()
    df_size.plot(kind="bar", ax=ax2)

    ax2.set_title("SLA2")
    ax2.set_xlabel("Conta")
    ax2.set_ylabel("Quantidade")

    plt.tight_layout()
    st.pyplot(fig2)
