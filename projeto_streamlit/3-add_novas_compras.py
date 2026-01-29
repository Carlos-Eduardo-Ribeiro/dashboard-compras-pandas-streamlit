from datetime import datetime
import streamlit as st
import pandas as pd
import ast

st.set_page_config(layout="wide")

st.markdown('# 📊 Sistema de Compras', text_alignment='center') # Definição de Título
st.markdown('## Cadastro de Compras')

# funções

def limpar():
    st.session_state.texto = ""

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

# criando novas colunas:
df_lojas['cidade/estado'] = df_lojas['cidade'] + '/' + df_lojas['estado']

# Elaborando lista e selecionando  de cidade/estado
lista_lojas = df_lojas['cidade/estado'].to_list()
loja_selecionada = st.sidebar.selectbox('selecione a loja:', lista_lojas)

# Elaborando lista e selecionando de vendedores baseados na loja seleciona
lista_vendedores =  ast.literal_eval(df_lojas.loc[df_lojas['cidade/estado'] == loja_selecionada, 'vendedores'].iloc[0])
vendepdor_selecionado = st.sidebar.selectbox('Selecione o vendedor:', lista_vendedores)

# Elaborando lista e selecionando de produtos
lista_produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o produto:', lista_produtos)

# Elaborando campo de input do nome dos clientes
nome_cliente = st.sidebar.text_input('Digite o nome do cliente:', key='texto')
#st.sidebar.button("Limpar", on_click=limpar)

# Elaborando selecionando gênero
genero_selecionado =  st.sidebar.selectbox('Selecione o gênero:', ['masculino', 'feminino'])

# Elaborando selecionando gênero
forma_pagamento_selecionado = st.sidebar.selectbox('Digite a forma de pagamento:', df_forma_pagamento['0'] )

# Gerando o dfframe renderizado no streamlit web com base nas indormações

if st.sidebar.button('Adicionar compra'):
    nova_compra = {
        'id_compra': 1 if df_compras.empty else df_compras['id_compra'].max() + 1,
        'loja': loja_selecionada,
        'vendedor': vendepdor_selecionado,
        'produto': produto_selecionado,
        'cliente_nome': nome_cliente,
        'cliente_genero': genero_selecionado,
        'forma_pagamento': forma_pagamento_selecionado
    }
    df_compras.loc[datetime.now()] = nova_compra

    df_compras.to_csv(caminho_compras, decimal=',', sep=';')

    st.success('Compra adicionada!')

st.dataframe(df_compras)