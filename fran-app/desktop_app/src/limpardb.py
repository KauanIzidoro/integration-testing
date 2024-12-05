# Importando os controladores e configurando a sessão
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Controllers.ItemSaleController import (
    ItemSaleController,  # Certifique-se de que o ItemSaleController está importado
)
from Controllers.ProductController import ProductController
from Controllers.StorageController import StorageController

# Configuração do banco de dados
engine = create_engine(
    'sqlite:///test.db'
)  # ou o caminho correto do seu banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a sessão
db = SessionLocal()

# Criando a instância do ItemSaleController
itemSaleController = ItemSaleController(session=db)
productController = ProductController(session=db)
storageController = StorageController(session=db)

# Limpando todos os registros da tabela ItemSale
itemSaleController.delete_all_items()
productController.delete_all_products()
storageController.delete_all_storage()
# Fechar a sessão depois de realizar a operação
db.close()
