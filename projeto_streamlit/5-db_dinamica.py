import pandas as pd
import streamlit as st
from datetime import timedelta

st.set_page_config(layout='wide')

# criando valores globais
PERC_COMISSAO = 0.05    
COLUNAS_ANALISE = ['loja', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
COLUNAS_NUMERICAS = ['preco', 'comissao']
FUNCOES_AGREGACAO = {'soma' : 'sum', 'contagem' : 'count'}

# caminhos dos arquivos
caminho_compras  = r'datasets\df_compras.csv'
caminho_loja = r'datasets\df_lojas.csv'
caminho_produtos = r'datasets\df_produtos.csv'
caminho_forma_pagamento = r'datasets\df_formas_pagamentos.csv'

# carregando dados
df_compras =  pd.read_csv(caminho_compras, sep=';', decimal=',', index_col=0,  parse_dates=True) 
df_lojas = pd.read_csv(caminho_loja, sep=';', decimal=',')
df_produtos = pd.read_csv(caminho_produtos, sep=';', decimal=',')
df_forma_pagamento =  pd.read_csv(caminho_forma_pagamento, sep=';', decimal=',') 

# renomeando colunas
df_produtos = df_produtos.rename(columns={'nome' : 'produto'})
print(df_produtos)

# resetando o index para ter melhaor organização
df_compras = df_compras.reset_index()

# rest do index
df_compras =  df_compras.set_index('data') # preciso resetar devido ao merge com outro df

# merge de df(s) compras e produtos
df_compras = df_compras.merge(right = df_produtos[['preco', 'produto']], on  ='produto', how = 'left')

# criando nova coluna de comissao
df_compras['comissao'] =  df_compras['preco'] * PERC_COMISSAO

# criando multiplas seleções
indice_dinamico = st.sidebar.multiselect('Selecione os indiceis:', COLUNAS_ANALISE)
colunas_filtradas =  [c for c in COLUNAS_ANALISE if not c in indice_dinamico]
coluna_dinamica = st.sidebar.multiselect('Selecione as colunas:', colunas_filtradas)
valor_analise = st.sidebar.selectbox('Selecione o valor:', COLUNAS_NUMERICAS)
metrica_analise = st.sidebar.selectbox('Selecione a metrica:', list(FUNCOES_AGREGACAO.keys()))

if len(indice_dinamico) > 0 and len(coluna_dinamica) > 0: 
    metrica =  FUNCOES_AGREGACAO[metrica_analise]
    compras_dinamica = pd.pivot_table(
        df_compras,
        index=indice_dinamico,
        columns=coluna_dinamica,
        values=valor_analise,
        aggfunc=metrica
    )
    compras_dinamica['TOTAL_GERAL'] = compras_dinamica.sum(axis=1)
    compras_dinamica.loc['TOTAL_GERAL'] = compras_dinamica.sum(axis=0).to_list()

    st.dataframe(compras_dinamica)