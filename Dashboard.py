import pandas as pd
import numpy as np 
import datetime
import time
import streamlit as st 
import altair as alt
from PIL import Image
#from streamlit_option_menu import option_menu
st.set_page_config(
    page_title = 'Dashboard Vendas - Leonardo Vargas',
    page_icon = '$',
    layout = 'wide', # centered ou wide
    initial_sidebar_state='expanded', # collapsed ou expanded ou auto,
    menu_items={
        'Get Help':'http://www.meusite.com.br',
        'Report a bug': 'http://www.meuoutrosite.com.br',
        'About':'Esse APP foi desenvolvido no nosso Curso.'
    }
)

######### Padrões Gráficos #########
cor_grafico = '#000000'

# Criação do Dataframe

df = pd.read_excel(
    io = './data/system_extraction.xlsx',
    engine = 'openpyxl',
    sheet_name = 'salesreport',
    usecols = 'A:J',
    nrows = 4400
)

# Criação do SideBar para os filtros
with st.sidebar:
    st.subheader('MENU - DASHBOARD VENDAS')
    fVendedor = st.selectbox(
        'Selecione o Vendedor: ',
        options = df['Vendedor'].unique()
    )
    fProduto = st.selectbox(
        'Selecione o Produto: ',
        options = df['Produto vendido'].unique(),

    )
    fCliente = st.selectbox(
        'Selecione o Cliente: ',
        options = df['Cliente'].unique()
    )

# Quantidade de Vendas Agrupada por Produto
vendas_agrupadas_produtos = df.loc[
    (df['Vendedor'] == fVendedor) 
    & (df['Cliente'] == fCliente)
]
vendas_agrupadas_produtos = vendas_agrupadas_produtos.groupby('Produto vendido').sum().reset_index()

grafico_vendas_agrupadas_produtos = alt.Chart(vendas_agrupadas_produtos).mark_bar(
    color = '#00BFFF',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Produto vendido'),
    y = 'Quantidade',
    tooltip = ['Produto vendido', 'Quantidade']
).properties(
    title = 'QUANTIDADE DE VENDAS POR PRODUTO'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)

grafico_valor_venda_agrupado_produtos = alt.Chart(vendas_agrupadas_produtos).mark_bar(
    color = '#00BFFF',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Produto vendido'),
    y = 'Valor Pedido',
    tooltip = ['Produto vendido', 'Valor Pedido']
).properties(
    title = 'VALOR TOTAL POR PRODUTO'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)


# Margem de Vendas
margem_de_vendas = df.loc[
    (df['Vendedor'] == fVendedor) 
    & (df['Produto vendido'] == fProduto)
    & (df['Cliente'] == fCliente)
]



# Vendas por Vendedor
vendas_por_vendedor = df.loc[
    (df['Produto vendido'] == fProduto)
    & (df['Cliente'] == fCliente)
]
vendas_por_vendedor = vendas_por_vendedor.groupby('Vendedor').sum().reset_index()
vendas_por_vendedor = vendas_por_vendedor[['Vendedor', 'Quantidade', 'Valor Pedido', 'Margem Lucro']]

grafico_vendas_agrupadas_por_vendedor = alt.Chart(vendas_por_vendedor).mark_bar(
    color = '#DAA520',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Vendedor'),
    y = 'Quantidade',
    tooltip = ['Vendedor', 'Quantidade']
).properties(
    title = 'QUANTIDADE DE VENDAS POR VENDEDOR'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)

grafico_valor_venda_agrupada_vendedor = alt.Chart(vendas_por_vendedor).mark_bar(
    color = '#DAA520',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Vendedor'),
    y = 'Valor Pedido',
    tooltip = ['Vendedor', 'Valor Pedido']
).properties(
    title = 'VALOR TOTAL POR VENDEDOR'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)

# Vendas por Cliente

vendas_por_cliente = df.loc[
    (df['Vendedor'] == fVendedor) 
    & (df['Produto vendido'] == fProduto)
]
vendas_por_cliente = vendas_por_cliente.groupby('Cliente').sum().reset_index()
vendas_por_cliente = vendas_por_cliente[['Cliente', 'Quantidade', 'Valor Pedido', 'Margem Lucro']]

grafico_vendas_agrupadas_clientes = alt.Chart(vendas_por_cliente).mark_bar(
    color = '#32CD32',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Cliente'),
    y = 'Quantidade',
    tooltip = ['Cliente', 'Quantidade']
).properties(
    title = 'QUANTIDADE DE VENDAS POR CLIENTE'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)

grafico_valor_venda_agrupado_clientes = alt.Chart(vendas_por_cliente).mark_bar(
    color = '#32CD32',
    cornerRadiusTopLeft = 9,
    cornerRadiusTopRight = 9
).encode(
    x = alt.X('Cliente'),
    y = 'Valor Pedido',
    tooltip = ['Cliente', 'Valor Pedido']
).properties(
    title = 'VENDAS POR CLIENTE'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)


# Vendas Mensais
vendas_mensais = df.loc[
    (df['Vendedor'] == fVendedor) 
    & (df['Produto vendido'] == fProduto)
    & (df['Cliente'] == fCliente)
]
vendas_mensais['cdmes'] = vendas_mensais['Data'].dt.month+vendas_mensais['Data'].dt.year*100
vendas_mensais['ano'] = vendas_mensais['Data'].dt.year

grafico_vendas_mensais = alt.Chart(vendas_mensais).mark_line(
    point = alt.OverlayMarkDef(color = 'green', size = 100, filled = False, fill = 'white'),
    color = '#FF4B4B'
).encode(
    alt.X('monthdate(Data):T'),
    y = 'Valor Pedido:Q'
).properties(
    title = 'VENDAS MENSAIS'
).configure_axis(
    grid = False
).configure_view(
    strokeWidth = 0
)

# Totais
total_vendas = round(margem_de_vendas['Valor Pedido'].sum(), 2)
total_margem = round(margem_de_vendas['Margem Lucro'].sum(), 2)
porc_margem = int((total_margem/total_vendas)*100)

# Página Principal
st.header(':bar_chart: DASHBOARD DE VENDAS')

# BIG NUMBERS
big_numbers_1, big_numbers_2, big_numbers_3 = st.columns([1, 1, 1])
with big_numbers_1:
    st.write('**VENDAS TOTAIS**')
    st.info(f'R$ {total_vendas}')
with big_numbers_2:
    st.write('**MARGEM TOTAL**')
    st.info(f'R$ {total_margem}')

with big_numbers_3:
    st.write('**MARGEM PERCENTUAL**')
    st.info(f'R$ {porc_margem}')

# Gráficos
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.subheader('Visão PRODUTOS')
    st.altair_chart(grafico_vendas_agrupadas_produtos, use_container_width = True)
    st.altair_chart(grafico_valor_venda_agrupado_produtos, use_container_width = True)
with col2:
    st.subheader('Visão VENDEDOR')
    st.altair_chart(grafico_vendas_agrupadas_por_vendedor, use_container_width = True)
    st.altair_chart(grafico_valor_venda_agrupada_vendedor, use_container_width = True)

with col3:
    st.subheader('Visão CLIENTE')
    st.altair_chart(grafico_vendas_agrupadas_clientes, use_container_width = True)
    st.altair_chart(grafico_valor_venda_agrupado_clientes, use_container_width = True)


st.subheader('Visão MENSAL')
st.altair_chart(grafico_vendas_mensais, use_container_width = True)

st.markdown('---')














