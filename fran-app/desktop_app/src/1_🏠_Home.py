import os

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Controllers.ProductController import ProductController
from models import table_registry

# Obtém o diretório onde o arquivo Python está localizado (no caso, dentro de 'src')
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construa o caminho completo para o banco de dados dentro da pasta 'src'
db_path = os.path.join(base_dir, 'test.db')

# Crie a conexão com o banco de dados SQLite
engine = create_engine(f'sqlite:///{db_path}')

table_registry.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Teste de criação de produtos no banco de dados local

productController = ProductController(session=db)

# productController.create_product(name='Suco',
#                                  description='descrição do suco',
#                                  price=12.90)

print(productController.list_products())

st.set_page_config(
    page_title='Home',
    page_icon='🍰',
    layout='wide',
)

# logo = '/mnt/c/fran-app/fran-app/desktop_app/src/assets/logo_cake.png'
# st.logo(logo)

# def test_create_product():
#     # Configura o banco de dados local (criará o arquivo test.db se não existir)
#     engine = create_engine('sqlite:///test.db')
#     table_registry.metadata.create_all(engine)
#     productController.create_product(name='Suco',description='descrição do suco',price=12.90)

#     # # Abre uma nova sessão para manipular o banco de dados
#     # with Session(engine) as session:
#     #     # Cria um novo produto
#     #     new_product = Product(
#     #         name='bolo', description='bolo de chocolate', price=99.90
#     #     )

#     #     # Adiciona o produto à sessão e persiste no banco de dados
#     #     # session.add(new_product)
#     #     # session.commit()

#     #     # Consulta o banco para verificar o produto criado
#     #     product = session.scalar(select(Product).where(Product.name == 'bolo'))

#     #     # Valida o nome do produto
#     #     assert product.name == 'bolo'
#     #     print(
#     #         'Produto criado com sucesso:',
#     #         product.name,
#     #         product.description,
#     #         product.price,
#     #     )


# if __name__ == '__main__':
#     test_create_product()
