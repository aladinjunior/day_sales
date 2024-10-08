import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

df = pd.read_csv("vendasatualizadas.csv")
# df
df["DATA"] = pd.to_datetime(df["DATA"])
# df["DATA"]

df["DIA"] = df["DATA"].apply(lambda x: str(x.day) + "/" + str(x.month))
# df

domingo = df[df["DIA DA SEMANA"] == "Domingo"]

ordem_dias = ["Domingo", "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"]

# Agrupar os dados pela coluna "DIA DA SEMANA" e somar o valor da coluna "TOTAL" para cada dia
totais_por_dia = df.groupby("DIA DA SEMANA")["TOTAL"].sum().reset_index()

# Definir a coluna "DIA DA SEMANA" como categórica com a ordem desejada
totais_por_dia["DIA DA SEMANA"] = pd.Categorical(totais_por_dia["DIA DA SEMANA"], categories=ordem_dias, ordered=True)

# Ordenar o DataFrame pela coluna "DIA DA SEMANA"
totais_por_dia = totais_por_dia.sort_values("DIA DA SEMANA")



# day = st.sidebar.selectbox("Dia", df["DIA"].unique())


companies = [" ","POSTO 1", "POSTO 2", "POSTO 3", "LIG COMBUSTIVEIS"]

company = st.sidebar.selectbox("Selecione a Empresa", companies)

# df_filtered = df[df["DIA"] == day]
# df_filtered

# Verificando se a opção "LIG COMBUSTIVEIS" foi selecionada
if company == "LIG COMBUSTIVEIS":
    # Exibir a média de combustíveis vendidos
    fuel_mean = round(df["TOTAL"].mean(), 2)

    col1, col2 = st.columns(2)

    # Gráfico de vendas por dia
    fig_date = px.bar(df, x="DATA", y="TOTAL", title="Total de Combustíveis Vendidos por Dia")
    col1.plotly_chart(fig_date)

    # Cálculo do total de cada combustível
    total_biodiesel = df["BIODIESEL BS10 COMUM"].sum()
    total_etanol = df["ETANOL COMUM"].sum()
    total_gasolina_aditivada = df["GASOLINA ADITIVADA"].sum()
    total_gasolina_comum = df["GASOLINA COMUM"].sum()

    total_fuel = [total_biodiesel, total_etanol, total_gasolina_aditivada, total_gasolina_comum]
    combustiveis = ['Biodiesel BS10 Comum', 'Etanol Comum', 'Gasolina Aditivada', 'Gasolina Comum']

    # Gráfico de pizza para os combustíveis mais vendidos
    fig_top_combustiveis_vendidos = px.pie(
        values=total_fuel, names=combustiveis, title="Top Combustíveis Mais Vendidos"
    )
    col2.plotly_chart(fig_top_combustiveis_vendidos)

    col3, col4 = st.columns(2)

    # Gráfico total de combustíveis vendidos no mês
    fig_vendas_combustivel_mes = px.bar(
        x=total_fuel, y=combustiveis, 
        labels={'x': "Totais", 'y': "Combustiveis"}, title="Total de Combustível Vendidos no Mês",
        orientation="h"
    )
    col3.plotly_chart(fig_vendas_combustivel_mes)

    # Gráfico de vendas por dia da semana
    fig_dia_da_semana = px.bar(totais_por_dia, x="DIA DA SEMANA", y="TOTAL", title="Vendas de Combustíveis por Dia da Semana")
    col4.plotly_chart(fig_dia_da_semana)

else:
    st.write("Não há dados disponíveis para esse posto")







# px.bar(data_frame=df_filtered)