import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import names

#Criando bases de dados para o projeto

pasta_datesets =  Path(__file__).parent / "../datasets"

pasta_datesets.mkdir(parents=True, exist_ok=True)

LOJAS = [
    {'estado' : 'SP', 'cidade' : 'São Paulo', 'vendedores' : ['Ana Oliveira', 'Lucas Pereira']},
    {'estado' : 'RJ', 'cidade' : 'Copa Cabana', 'vendedores' : ['Carlos Silva', 'Luis Costa']},
    {'estado' : 'MG', 'cidade' : 'Belo Horizonte', 'vendedores' : ['Joana Silva', 'Olivia Sousa']},
    {'estado' : 'SC', 'cidade' : 'Florianopoles', 'vendedores' : ['Isabale Gomes', 'Paulo de Sousa']},
    {'estado' : 'PE', 'cidade' : 'Recife', 'vendedores' : ['João Victor', 'Bruno Otavio']}
]

PRODUTOS = [
    {'nome' : 'Smartphone Sansung Galaxy', 'id' : 0, 'preco' : 2650},
    {'nome' : 'Geladeira Sansung', 'id' : 1, 'preco' : 3245},
    {'nome' : 'Smartwatch Sansung M3', 'id' : 2, 'preco' : 450},
    {'nome' : 'Cama Solteiro Ortobom', 'id' : 3, 'preco' : 1458},
    {'nome' : 'Playstation 5', 'id' : 4, 'preco' : 3560}
]

FORMA_PAGAMENTO = ['cartão de crédito', 'boleto', 'pix', 'dinheiro']

GENERO_CLIENTE = ['male', 'female']

compras = []

for i in range(2000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja['vendedores'])
    produto =  random.choice(PRODUTOS)
    hora_compra = datetime.now() - timedelta(days =  random.randint(1, 365), hours = random.randint(-5, 5), minutes= random.randint(-30, 30))
    genero_cliente = random.choice(GENERO_CLIENTE)
    nome_cliente = names.get_full_name(genero_cliente)
    forma_pagamento = random.choice(FORMA_PAGAMENTO)

    compras.append(
        {
            'data' : hora_compra,
            'id_compra' : i,
            'loja' : loja['cidade'],
            'vendedor' : vendedor,
            'produto' : produto['nome'],
            'cliente_nome' : nome_cliente,
            'cliente_genero' : genero_cliente.replace('male' , 'masculino').replace('female' , 'feminino'),
            'forma_pagamento' :  forma_pagamento 

        }
    )

#Gerando df(s)

df_compras = pd.DataFrame(compras).set_index('data')
df_lojas = pd.DataFrame(LOJAS)
df_forma_pagamento = pd.DataFrame(FORMA_PAGAMENTO)
df_produtos = pd.DataFrame(PRODUTOS)

#Exportando df(s) para csv(s)

df_compras.to_csv(pasta_datesets / 'df_compras.csv', decimal=',', sep=';')
df_lojas.to_csv(pasta_datesets / 'df_lojas.csv', decimal=',', sep=';')
df_forma_pagamento.to_csv(pasta_datesets / 'df_formas_pagamentos.csv', decimal=',', sep=';')
df_produtos.to_csv(pasta_datesets / 'df_produtos.csv', decimal=',', sep=';')

#Exportar df(s) para xlsx(s)

df_compras.to_excel(pasta_datesets / 'df_compras.xlsx') #Obs: Os constants "decimal" e "sep" não funcionão em arquivos xlsx
df_lojas.to_excel(pasta_datesets / 'df_lojas.xlsx')
df_forma_pagamento.to_excel(pasta_datesets / 'df_formas_pagamentos.xlsx')
df_produtos.to_csv(pasta_datesets / 'df_produtos.xlsx', decimal=',', sep=';')


