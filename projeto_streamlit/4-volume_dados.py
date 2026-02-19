import pandas as pd
import streamlit as st
from datetime import timedelta

st.set_page_config(layout='wide')

st.markdown('# Sistema de Compras', text_alignment='center')
st.markdown('## Números Gerais')

# Definindo funções de session_state

def limpar_datas():
    st.session_state['data_inicio'] = data_inicial_default
    st.session_state['data_final'] = data_final_default

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

#Inicializando a widget
if 'data_inicio' not in st.session_state:
    st.session_state['data_inicio'] = data_inicial_default

if 'data_final' not in st.session_state:
    st.session_state['data_final'] = data_final_default

# Definindo suas estruturas no streamlit
data_inicio = st.sidebar.date_input(
    'Data inicial:',
    format='DD/MM/YYYY',
    key='data_inicio'
)

data_final = st.sidebar.date_input(
    'Data final:',
    format='DD/MM/YYYY',
    key='data_final'
)

# Crinado botão de lipar data baseada na session_state
st.sidebar.button('Limpar seleção', on_click=limpar_datas)

#Lógica de filtro para a tabela
df_compras_filtrado = df_compras[(df_compras.index.date >= data_inicio) & (df_compras.index.date <=data_final)]

#Atribuindo colunas para metricas
col1, col2 = st.columns(2)

#criando e formatando valores de cards
Valor_compras = df_compras_filtrado['preco'].sum()
Valor_compras = f"R$ {Valor_compras:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

Quantidade_compras = df_compras_filtrado['preco'].count()
Quantidade_compras = f"{Quantidade_compras:,.0f}".replace(",", ".")

# Add cards
col1.metric('Valor de compras do pedido', Valor_compras)
col2.metric('Quantidade de compras no período', Quantidade_compras)

# Sempre usar uma seguimentação em decorrência da outra para aplicações d multiplas seguimentações

# Add uma linha divisoria
st.divider()

# Criando marckdown com a loja com mais compras
principal_loja = df_compras_filtrado['loja'].value_counts().index[0]
st.markdown(f'## Principal Loja: {principal_loja}')

#Atribuindo colunas para metricas
col21, col22 = st.columns(2)

#Criando o valor e quantidade vendida pela loja com mais value_counts
Valor_compras_loja = df_compras_filtrado[df_compras_filtrado['loja'] == principal_loja]['preco'].sum()
Valor_compras_loja = f"R$ {Valor_compras_loja:,.2f}".replace(',', '.')
Quantidade_compras_lojas = df_compras_filtrado[df_compras_filtrado['loja'] == principal_loja]['preco'].count()
Quantidade_compras_lojas = f"{Quantidade_compras_lojas:,.0f}".replace(',', '.')

# Add cards
col21.metric("Valor de compras no período", Valor_compras_loja)
col22.metric("Quantidade de compras no período", Quantidade_compras_lojas)

# Add uma linha divisoria
st.divider()

principal_vendedor = df_compras_filtrado['vendedor'].value_counts().index[0]
st.markdown(f'## Principal Vendedor: {principal_vendedor}')

#Atribuindo colunas para metricas
col31, col32 = st.columns(2)

# Criando o valor e quantidade de compras por vendedor

Valor_compras_vendedor =  df_compras_filtrado[df_compras_filtrado['vendedor'] == principal_vendedor]['preco'].sum()
Valor_compras_vendedor = f'R$ {Valor_compras_vendedor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
Valor_comissao_vendedor = df_compras_filtrado[df_compras_filtrado['vendedor'] == principal_vendedor]['comissao'].sum()
Valor_comissao_vendedor = f'R$ {Valor_comissao_vendedor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Add cards
col31.metric('Valor de vendas no período', Valor_compras_vendedor)
col32.metric('Comissão de vendas no período', Valor_comissao_vendedor)