import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("VULC3_evolucao.xlsx")
print(df)

df["valor"].max()
df["valor"].min()
df["valor"].mean()
df["valor"].std()

df[0:1]

colunas = ["conta", "valor"]
df[23:24][colunas]

linhas = df["trimestre"] == "202621"
colunas = ["conta", "valor"]
df[linhas][colunas]

linhas = df["conta"] == "lucro"
colunas = ["valor"]
df[linhas][colunas].mean()

linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df[linhas][colunas]
sns.lineplot(dados, x='trimestre', y='valor')
plt.title("Grafico Lucro")
plt.xticks(rotation=45)