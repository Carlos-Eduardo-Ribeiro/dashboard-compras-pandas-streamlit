import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Filtro de Compras") # Definição de Título

df_compras = pd.read_csv( r'datasets\df_compras.csv', sep=';', decimal=',', index_col=0) # Carga dos dados

colunas = list(df_compras.columns) #Criando seleção de colunas
colunas_selecionadas = st.sidebar.multiselect("Selecione as colunas:", colunas, default=colunas) # printa uma seleceção multiplas de coluna

# Crinado sidebar(s)

col1, col2 = st.sidebar.columns(2)

# Determinando possíveis valores selecionaveis

col_filtro =  col1.selectbox("Selecione a coluna:", [c for c in colunas if c not in["id_compra"]])
valor_filtro = col2.selectbox("Selecione os valores", list(df_compras[col_filtro].unique()))

# Definindo valores selecionados pelo botão

st_filter = col1.button("Aplicar Filtro")
st_limpar = col2.button("Limpar Filtro")

# Aplicando os filtros na base de dados

if st_filter:
    st.dataframe(df_compras.loc[df_compras[col_filtro] == valor_filtro, colunas_selecionadas])
elif st_limpar:
    st.dataframe(df_compras[colunas_selecionadas])
else:
    st.dataframe(df_compras[colunas_selecionadas])

