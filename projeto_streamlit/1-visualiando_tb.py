import pandas as pd
import streamlit as st

# O streamlit é feito par aa criação de dataapps(aplicações web) sem necessidade do uso de html, css, javascript/typescript

st.set_page_config(layout="wide")
st.title("Visualização de Compras") # Definição de Título

caminho_compras  = r'datasets\df_compras.csv'

df_compras =  pd.read_csv(caminho_compras, sep=';', decimal=',')

print(df_compras) # printa do terminal

st.dataframe(df_compras) # printa no streamlit web

# -m é uma indicação de acesso a um modulo do python
# Rodar o arquivo com stremlt no localhost "python -m streamlit run .\caminho do aquivo"
# Ctrl c encerra o processo do streamlit no terminal

