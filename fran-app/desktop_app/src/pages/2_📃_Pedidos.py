import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Controllers.ItemSaleController import ItemSaleController
from Controllers.ProductController import ProductController
from Controllers.SaleController import SaleController
from Controllers.StorageController import StorageController
from models import table_registry

# Configurações do banco de dados

# Obtém o diretório onde o arquivo Python está localizado (no caso, dentro de 'src')
base_dir = os.path.dirname(os.path.abspath(__file__))

# Subir um nível de diretório para alcançar 'src' e criar o banco de dados lá
db_path = os.path.join(base_dir, '..', 'test.db')

# Crie a conexão com o banco de dados SQLite
engine = create_engine(f'sqlite:///{db_path}')

table_registry.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
productController = ProductController(session=db)
storageController = StorageController(session=db)
saleController = SaleController(
    session=db, storage_controller=storageController
)  # Adiciona o storageController aqui
itemSaleController = ItemSaleController(session=db)


# TODO: Reaproveitamento de funções semelhantes.

st.set_page_config(
    page_title='Pedidos',
    page_icon='🍰',
    layout='wide',
)

# logo = '/mnt/c/fran-app/fran-app/desktop_app/src/assets/logo_cake.png'
# st.logo(logo)

st.markdown("""
    # 📃 Pedidos
""")

# Inicializar a lista de produtos no session_state
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# Inicializar st.session_state.df com dados do banco de dados, se não estiver inicializado
if 'df' not in st.session_state or st.session_state.df.empty:
    products = (
        productController.list_products()
    )  # Método para buscar produtos do banco de dados
    st.session_state.df = pd.DataFrame(
        products, columns=['id', 'name', 'price', 'description']
    )


@st.dialog('Fechar Pedido', width='small')
def fechar_pedido():
    # Título
    st.markdown('### Finalizar Pedido')
    st.divider()

    # Forma de pagamento
    forma_pagamento = st.radio(
        'Escolha a forma de pagamento:',
        ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'Pix'],
        index=0,
    )

    # Exibir o total do pedido
    if 'carrinho' in st.session_state and st.session_state.carrinho:
        total = sum(
            product['price'] * product['quantity']
            for product in st.session_state.carrinho
        )
        st.markdown(f'### Total do Pedido: R$ {total:.2f}')
    else:
        total = 0
        st.markdown('### Carrinho está vazio.')

    # Variáveis para controle
    valor_entrada = None
    troco = None
    pode_confirmar = True  # Por padrão, o botão está habilitado

    # Se a forma de pagamento for "Dinheiro", exigir o valor de entrada
    if forma_pagamento == 'Dinheiro':
        valor_entrada = st.number_input(
            'Digite o valor pago:', min_value=0.0, value=0.0, step=0.01
        )
        if valor_entrada >= total:
            troco = valor_entrada - total
            st.markdown(f'**Troco:** R$ {troco:.2f}')
        else:
            pode_confirmar = False  # O botão de confirmar ficará desabilitado
            st.warning(
                'O valor pago é menor que o total do pedido. Por favor, insira um valor maior.'
            )

    # Botão para confirmar o pedido
    confirmar = st.button(
        'Confirmar Pedido', disabled=(not pode_confirmar or total <= 0)
    )

    if confirmar and total > 0:
        if forma_pagamento == 'Dinheiro' and valor_entrada < total:
            st.error('O valor pago é insuficiente para finalizar o pedido.')
        else:
            try:
                # Validar estoque antes de processar a venda
                for product in st.session_state.carrinho:
                    product_id = product['id']
                    quantity = product['quantity']
                    estoque_atual = storageController.get_stock(product_id)
                    if estoque_atual < quantity:
                        raise ValueError(
                            f'Estoque insuficiente para o produto: {product["name"]}'
                        )

                # Criar a venda e processar os itens
                item_sales = [
                    {
                        'product_id': product['id'],
                        'quantityItem': product['quantity'],
                    }
                    for product in st.session_state.carrinho
                ]
                saleController.create_sale(
                    total_sale=total,
                    item_sales=item_sales,
                    storage_controller=storageController,
                )
                st.success(
                    f'Pedido fechado com sucesso! Forma de pagamento: {forma_pagamento}.'
                )
                st.session_state.carrinho.clear()
                st.rerun()
            except ValueError as ve:
                st.error(str(ve))
            except Exception as e:
                st.error(f'Erro ao registrar a venda: {str(e)}')

    elif confirmar:
        st.error('Não há itens no carrinho para finalizar o pedido.')

    # Botão para cancelar o pedido
    if st.button('Cancelar'):
        st.warning('Pedido cancelado.')
        st.session_state.carrinho.clear()  # Limpa o carrinho
        st.rerun()  # Atualiza a interface


# Função para mostrar os produtos no carrinho logo abaixo do título
def mostrar_carrinho():
    if len(st.session_state.carrinho) > 0:
        col1, col2, col3 = st.columns([7, 1, 1])
        with col1:
            st.write('### Produtos no Carrinho:')
        with col2:
            if st.button('Limpar Carrinho', key='limpar_carrinho'):
                st.session_state.carrinho.clear()
                st.rerun()
        with col3:
            if st.button('Fechar Pedido', key='fechar_pedido'):
                fechar_pedido()

        total = sum(
            product['price'] * product['quantity']
            for product in st.session_state.carrinho
        )
        with st.container(border=True, height=150):
            for product in st.session_state.carrinho:
                st.write(
                    f'{product["name"]} - R$ {product["price"]:.2f} (Quantidade: {product["quantity"]})'
                )
            st.markdown(f'### **Total: R$ {total:.2f}**')

    else:
        st.write('Não há produtos no carrinho.')


# Chama a função para mostrar o carrinho logo após o título
mostrar_carrinho()


def mostrar_pedido():
    st.text_input('Pesquise o produto aqui: ')

    with st.container(border=True, height=450):
        for index, row in st.session_state.df.iterrows():
            product_name = row['name']
            product_id = row['id']
            product_price = row['price']

            col1, col2, col3, col4 = st.columns(4)

            # estilização do botão
            st.markdown(
                """
                            <style>
                                .stButton>button {
                                    height: 60px;  /* Aumenta a altura do botão */
                                    font-size: 20px;  /* Ajusta o tamanho da fonte */
                                    border-radius: 12px;  /* Bordas arredondadas */
                                }
                                .stButton>button:hover {
                                    background-color: #white;  /* Cor de fundo ao passar o mouse */
                                }
                            </style>
                        """,
                unsafe_allow_html=True,
            )

            # Coluna de visualização de produtos
            with col1:
                st.write(f'{product_id} - {product_name}')
                st.markdown(
                    '<hr style="border: 2px solid #4CAF50;">',
                    unsafe_allow_html=True,
                )

            with col2:
                st.write(f'**Preço** R$ {product_price}')
                st.markdown(
                    '<hr style="border: 2px solid #B0C4DE;">',
                    unsafe_allow_html=True,
                )

            with col3:
                if st.button(
                    ' Adicionar ',
                    key=f'Adicionar_{product_id}',
                    use_container_width=True,
                ):
                    # Verificar se o produto já está no carrinho
                    produto_existente = next(
                        (
                            p
                            for p in st.session_state.carrinho
                            if p['id'] == product_id
                        ),
                        None,
                    )
                    if produto_existente:
                        produto_existente['quantity'] += (
                            1  # Incrementar a quantidade se já estiver no carrinho
                        )
                    else:
                        # Adicionar novo produto com quantidade inicial 1
                        st.session_state.carrinho.append({
                            'id': product_id,
                            'name': product_name,
                            'price': product_price,
                            'quantity': 1,
                        })
                    st.success(
                        f'Produto "{product_name}" adicionado ao carrinho!'
                    )
                    st.rerun()

            with col4:
                if st.button(
                    ' Retirar ',
                    key=f'Retirar_{product_id}',
                    type='primary',
                    use_container_width=True,
                ):
                    produto_existente = next(
                        (
                            p
                            for p in st.session_state.carrinho
                            if p['id'] == product_id
                        ),
                        None,
                    )
                    if produto_existente:
                        if produto_existente['quantity'] > 1:
                            produto_existente['quantity'] -= (
                                1  # Reduzir a quantidade
                            )
                        else:
                            # Remover produto do carrinho se a quantidade for 1
                            st.session_state.carrinho.remove(produto_existente)
                        st.warning(
                            f'Produto "{product_name}" atualizado no carrinho!'
                        )
                    else:
                        st.warning('Produto não encontrado no carrinho.')
                    st.rerun()


mostrar_pedido()
