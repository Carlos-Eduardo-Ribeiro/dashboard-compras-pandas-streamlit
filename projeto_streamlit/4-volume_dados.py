import pandas as pd
import streamlit as st
from datetime import timedelta

st.set_page_config(layout='wide')

st.markdown('# Sistema de Compras', text_alignment='center')
st.markdown('## Lista de compras', text_alignment='center')

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

# merge left de df(s)
df_compras = df_compras.merge(right = df_produtos[['preco', 'produto']], on  ='produto', how = 'left')

# rest do index
df_compras =  df_compras.set_index('data') # preciso resetar devido ao merge com outro df

#Criando nova coluna de comissao
df_compras['comissao'] =  df_compras['preco'] * 0.05

#criar as data de inicio
data_inicial_default =  df_compras.index.min().date()
data_final_default = df_compras.index.max().date()

#Ddefinindo suas estruturas no streamlit
data_inicio =  st.sidebar.date_input('Data inicial:', data_inicial_default, format='DD/MM/YYYY')
data_final = st.sidebar.date_input('Data final:', data_final_default, format='DD/MM/YYYY')

#Lógica de filtro para a tabela
df_compras_filtrado = df_compras[(df_compras.index.date >= data_inicio) & (df_compras.index.date <=data_final)]

#criando cards
total = df_compras_filtrado['preco'].sum()
total_formatado = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 1px;               
        border-radius: 20px;         
        color: black;                
        width: 250px;
        text-align: center;
        margin : 10px;
        ">
        <h4 style= "text-align: center;">Total de Compras</h4>
        <p style="font-size: 24px; font-weight: bold;">{total_formatado}</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button('Aplicar filtro'):
    st.dataframe(df_compras_filtrado)
else:
    st.dataframe(df_compras)

