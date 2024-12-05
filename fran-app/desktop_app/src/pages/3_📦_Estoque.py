# Este arquivo contém a página de cadastro de produtos
import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Controllers.ProductController import ProductController
from Controllers.StorageController import StorageController
from models import Storage, table_registry

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

# TODO: Reaproveitamento de funções semelhantes.

st.set_page_config(
    page_title='Estoque',
    page_icon='🍰',
    layout='wide',
)

# logo = '/mnt/c/fran-app/fran-app/desktop_app/src/assets/logo_cake.png'
# st.logo(logo)

st.write("""
# Controle de Estoque
Gerenciamento de produtos
""")

# Carregar o DataFrame no session_state se não existir
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(productController.list_products())


def update_dataframe():
    st.session_state.df = pd.DataFrame(productController.list_products())


@st.dialog('Cadastro de Produto', width='small')
def cadastro_produto():
    nome = st.text_input('Nome do Produto')
    descricao = st.text_input('Descrição do Produto')
    preco = st.text_input('Preço do Produto')
    qtd = st.text_input('Quantidade do Produto')
    submit_button = st.button('Cadastrar Produto')

    if submit_button:
        try:
            # Validação de campos
            if not nome or not descricao or not preco or not qtd:
                st.warning('Todos os campos são obrigatórios.')
                return

            if float(preco) <= 0 or int(qtd) <= 0:
                st.warning('Preço e quantidade devem ser maiores que zero.')
                return

            # Criar o produto
            new_product = productController.create_product(
                name=nome,
                description=descricao,
                price=float(preco),
            )
            # Registrar no estoque
            storageController.create_registry(
                product_id=new_product.product_id,
                cost=float(preco),
                quantity=int(qtd),
            )
            st.success('Produto cadastrado com sucesso!')
            update_dataframe()
            st.rerun()
        except ValueError as e:
            st.error(f'Erro: {str(e)}')


@st.dialog('Editar Produto', width='small')
def editar_produto(product_id):
    # Recupera os dados do produto a partir do ID
    product = productController.get_product_by_id(product_id)
    storage = db.query(Storage).filter_by(product_id=product_id).first()

    nome = st.text_input('Nome do Produto', value=product.name)
    descricao = st.text_input(
        'Descrição do Produto', value=product.description
    )
    preco = st.text_input('Preço do Produto', value=str(product.price))
    quantidade = st.text_input(
        'Quantidade', value=str(storage.quantity if storage else 0)
    )
    submit_button = st.button('Editar')

    if submit_button:
        try:
            # Validação d campos
            if not nome or not descricao or not preco or not quantidade:
                st.warning('Todos os campos são obrigatórios.')
                return

            if float(preco) <= 0 or int(quantidade) <= 0:
                st.warning('Preço e quantidade devem ser maiores que zero.')
                return

            # Atualizar o produto
            productController.update_product(
                product_id=product_id,
                name=nome,
                description=descricao,
                price=float(preco),
            )

            # Atualizar o registro de estoque
            if storage:
                storage.quantity = int(quantidade)
                storage.cost = float(preco)
            else:
                storageController.create_registry(
                    product_id=product_id,
                    quantity=int(quantidade),
                    cost=float(preco),
                )

            db.commit()
            st.success('Produto editado com sucesso!')
            update_dataframe()
            st.rerun()
        except ValueError as e:
            st.error(f'Erro: {str(e)}')


col1, col2, col3 = st.columns([3, 0.5, 1])

with col1:
    title = st.text_input('Busque um produto aqui:')

with col2:
    popover = st.popover('Filtros')
    per_desc = popover.selectbox(
        'Descrições',
        ('Sobremesa', 'Bebidas', 'Salgados'),
    )
    per_price = popover.slider('Preço', 0, 130, 25)


with col3:
    if st.button('Cadastrar Novo Produto'):
        cadastro_produto()


def delete_product(product_id):
    productController.delete_product(product_id)
    update_dataframe()
    st.success('Produto deletado com sucesso!')
    st.rerun()


st.subheader('Produtos cadastrados')

# botões de exclusão
for index, row in st.session_state.df.iterrows():
    product_name = row['name']
    product_id = row['id']
    product_price = row['price']
    product_desc = row['description']

    # Coluna de visualização de produtos
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 0.5, 0.6])

    with col1:
        st.write(f'{product_id} - {product_name}')
        st.markdown(
            '<hr style="border: 2px solid #4CAF50;">', unsafe_allow_html=True
        )

    with col2:
        st.write(f'*Descrição*: {product_desc}')
        st.markdown(
            '<hr style="border: 2px solid #FF6347;">', unsafe_allow_html=True
        )

    with col3:
        st.write(f'**Preço** R$ {product_price}')
        st.markdown(
            '<hr style="border: 2px solid #B0C4DE;">', unsafe_allow_html=True
        )

    with col4:
        if st.button('Editar', key=f'Editar_{product_id}'):
            st.session_state['editing_product_id'] = product_id
            editar_produto(product_id)

    with col5:
        if st.button('Deletar', key=f'Deletar_{product_id}', type='primary'):
            delete_product(product_id)
