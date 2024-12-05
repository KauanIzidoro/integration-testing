# Implementação do 'Facade' Pattern para os controllers da aplicação
from sqlalchemy.orm import Session

from Controllers.ItemSaleController import ItemSaleController
from Controllers.ProductController import ProductController
from Controllers.SaleController import SaleController
from Controllers.StorageController import StorageController
from models import ItemSale, Product, Sale, Storage


class IntegrationFacade:
    def __init__(self, session: Session):
        """
        Inicializa a facade com uma sessão SQLAlchemy e os controladores necessários.
        :param session: Instância de Session do SQLAlchemy.
        """
        self.session = session
        self.storage_controller = StorageController(session)
        self.sale_controller = SaleController(session, self.storage_controller)
        self.product_controller = ProductController(session)
        self.item_sale_controller = ItemSaleController(session)

    # Métodos de Produtos
    def create_product(
        self, name: str, description: str, price: float
    ) -> Product:
        return self.product_controller.create_product(name, description, price)

    def get_product(self, product_id: int) -> Product:
        return self.product_controller.get_product_by_id(product_id)

    def list_products(self) -> list[Product]:
        return self.product_controller.list_products()

    def delete_product(self, product_id: int):
        self.product_controller.delete_product(product_id)

    # Métodos de Estoque
    def add_to_storage(
        self, product_id: int, quantity: int, cost: float
    ) -> Storage:
        return self.storage_controller.create_registry(
            product_id, quantity, cost
        )

    def update_storage(
        self, product_id: int, quantity: int = None, cost: float = None
    ) -> Storage:
        return self.storage_controller.update_registry(
            product_id, quantity, cost
        )

    def get_storage(self, product_id: int) -> int:
        return self.storage_controller.get_stock(product_id)

    def list_storage(self) -> list[dict]:
        return self.storage_controller.list_storage()

    # Métodos de Vendas
    def create_sale(self, total_sale: float, item_sales: list[dict]) -> Sale:
        return self.sale_controller.process_sale(total_sale, item_sales)

    def list_sales(self) -> list[Sale]:
        return self.sale_controller.list_sales()

    def get_sale_details(self, sale_id: int) -> dict:
        sale = self.sale_controller.get_sale_by_id(sale_id)
        items = self.item_sale_controller.get_items_by_sale_id(sale_id)
        return {
            'sale_id': sale.sale_id,
            'total_sale': sale.total_sale,
            'items': [
                {'product_id': item.product_id, 'quantity': item.quantityItem}
                for item in items
            ],
        }

    # Métodos de Itens de Venda
    def create_item_sale(
        self, sale_id: int, product_id: int, quantity_item: int
    ) -> ItemSale:
        return self.item_sale_controller.create_item_sale(
            sale_id, product_id, quantity_item
        )

    def list_all_item_sales(self) -> list[ItemSale]:
        return self.item_sale_controller.list_all_items()
