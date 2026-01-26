from datetime import datetime
import streamlit as st
import pandas as pd

# caminhos dos arquivos

caminho_compras  = r'datasets\df_compras.csv'
caminho_loja = r'datasets\df_lojas.csv'
caminho_produtos = r'datasets\df_produtos.csv'

# carregando dados

df_compras =  pd.read_csv(caminho_compras, sep=';', decimal=',')
df_lojas = pd.read_csv(caminho_loja, sep=';', decimal=',')
df_produtos = pd.read_csv(caminho_produtos, sep=';', decimal=',')

# criando novas colunas:

df_lojas['cidade/estado'] = df_lojas['cidade'] + '/' + df_lojas['estado']
lista_lojas = df_lojas['cidade/estado'].to_list()
loja_selecionada = st.sidebar.selectbox('selecione a loja:', lista_lojas)

lista_vendedores =  df_lojas.loc[df_lojas['cidade/estado'] == loja_selecionada, 'vendedores'].iloc[0]
#st.write(lista_vendedores)
lista_vendedores = lista_vendedores.strip('][').replace("'",'').split(',')