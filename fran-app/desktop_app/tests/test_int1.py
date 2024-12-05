import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.Controllers.ProductController import ProductController
from src.Controllers.StorageController import StorageController
from src.models import table_registry

# Configurações do banco de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'test.db')
engine = create_engine(f'sqlite:///{db_path}')

table_registry.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
productController = ProductController(session=db)
storageController = StorageController(session=db)


def test_CriarProdutoEmEstoque():
    test_product_name = 'Produto de teste 1'
    test_product_price = 10.99
    test_product_description = 'Descrição do produto teste'
    test_product_quantity = 99
    test_product_cost = test_product_price * 0.2

    test_product = productController.create_product(
        name=test_product_name,
        description=test_product_description,
        price=test_product_price,
    )

    storageController.create_registry(
        product_id=test_product.product_id,
        cost=test_product_cost,
        quantity=test_product_quantity,
    )
    # Validação do produto
    assert test_product.name == test_product_name
    assert test_product.description == test_product_description
    assert test_product.price == test_product_price
    # # Validação do registro de estoque
    storage_entry = storageController.get_registry_by_id(
        test_product.product_id
    )
    assert storage_entry.cost == test_product_cost
    assert storage_entry.quantity == test_product_quantity


def test_VerificarProdutoCriadoEmEstoque():
    test_product_name = 'Produto de teste 1'
    test_product_price = 10.99
    test_product_description = 'Descrição do produto teste'
    test_product_quantity = 99
    test_product_cost = test_product_price * 0.2

    test_product = productController.create_product(
        name=test_product_name,
        description=test_product_description,
        price=test_product_price,
    )

    storageController.create_registry(
        product_id=test_product.product_id,
        cost=test_product_cost,
        quantity=test_product_quantity,
    )
    # Validação do produto
    assert test_product.name == test_product_name
    assert test_product.description == test_product_description
    assert test_product.price == test_product_price
    # # Validação do registro de estoque
    storage_entry = storageController.get_registry_by_id(
        test_product.product_id
    )
    assert storage_entry.entry_id == test_product.product_id
    assert storage_entry.cost == test_product_cost
    assert storage_entry.quantity == test_product_quantity
