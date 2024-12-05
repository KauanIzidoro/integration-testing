# ItemSale Controller
from sqlalchemy.orm import Session

from models import ItemSale


class ItemSaleController:
    def __init__(self, session: Session):
        """
        Inicializa o controlador com uma sessão SQLAlchemy.
        :param session: Instância de Session do SQLAlchemy.
        """
        self.session = session

    def create_item_sale(
        self, sale_id: int, product_id: int, quantity_item: int
    ) -> ItemSale:
        """
        Cria um novo registro de ItemSale associado a uma venda.
        :param sale_id: ID da venda.
        :param product_id: ID do produto.
        :param quantity_item: Quantidade do item vendido.
        :return: O ItemSale criado.
        """
        new_item_sale = ItemSale(
            sale_id=sale_id, product_id=product_id, quantityItem=quantity_item
        )
        self.session.add(new_item_sale)
        self.session.commit()
        return new_item_sale

    def get_items_by_sale_id(self, sale_id: int) -> list[ItemSale]:
        """
        Retorna todos os itens de venda associados a uma venda específica.
        :param sale_id: ID da venda.
        :return: Lista de itens de venda.
        """
        items = self.session.query(ItemSale).filter_by(sale_id=sale_id).all()
        return items

    def update_item_quantity(
        self, item_id: int, new_quantity: int
    ) -> ItemSale:
        """
        Atualiza a quantidade de um item vendido.
        :param item_id: ID do registro de ItemSale.
        :param new_quantity: Nova quantidade do item.
        :return: O ItemSale atualizado.
        :raises: NoResultFound se o item não for encontrado.
        """
        item = (
            self.session.query(ItemSale).filter_by(itemsale_id=item_id).one()
        )
        item.quantityItem = new_quantity
        self.session.commit()
        return item

    def delete_item_sale(self, item_id: int) -> None:
        """
        Deleta um registro de ItemSale pelo ID.
        :param item_id: ID do ItemSale.
        :raises: NoResultFound se o item não for encontrado.
        """
        item = (
            self.session.query(ItemSale).filter_by(itemsale_id=item_id).one()
        )
        self.session.delete(item)
        self.session.commit()

    def delete_all_items(self) -> None:
        """
        Deleta todos os itens de vendas na tabela ItemSale.
        :raises: Exception se ocorrer algum erro durante a exclusão.
        """
        try:
            # Deleta todos os registros da tabela ItemSale
            self.session.query(ItemSale).delete()
            self.session.commit()
            print('Todos os itens de venda foram deletados com sucesso.')
        except Exception as e:
            self.session.rollback()
            print(f'Erro ao deletar todos os itens de venda: {e}')

    def list_all_items(self) -> list[ItemSale]:
        """
        Lista todos os registros de ItemSale no banco de dados.
        :return: Lista de instâncias de ItemSale.
        """
        items = self.session.query(ItemSale).all()
        return items
