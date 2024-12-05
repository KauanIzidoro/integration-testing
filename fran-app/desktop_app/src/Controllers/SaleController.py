from sqlalchemy.orm import Session

from Controllers.StorageController import (
    StorageController,  # Importar o controlador de estoque
)
from models import ItemSale, Sale


class SaleController:
    def __init__(
        self, session: Session, storage_controller: StorageController
    ):
        """
        Inicializa o controlador com uma sessão SQLAlchemy e um controlador de estoque.
        :param session: Instância de Session do SQLAlchemy.
        :param storage_controller: Instância do controlador de estoque.
        """
        self.session = session
        self.storage_controller = storage_controller

    def create_sale(
        self,
        total_sale: float,
        item_sales: list[dict],
        storage_controller: StorageController,
    ) -> Sale:
        """
        Cria uma nova venda no banco de dados e atualiza o estoque.
        :param total_sale: Total da venda.
        :param item_sales: Lista de dicionários contendo as informações dos itens de venda (product_id, quantityItem).
        :param storage_controller: Instância do StorageController para manipular o estoque.
        :return: A venda criada.
        """
        try:
            # Criar a venda
            new_sale = Sale(total_sale=total_sale)
            self.session.add(new_sale)
            self.session.commit()  # Comita para obter o ID da venda

            # Criar registros de ItemSale associados à venda
            for item in item_sales:
                product_id = item['product_id']
                quantity_sold = item['quantityItem']

                # Atualiza o estoque antes de registrar a venda
                storage_controller.update_stock(product_id, -quantity_sold)

                # Criar item da venda
                new_item_sale = ItemSale(
                    sale_id=new_sale.sale_id,
                    product_id=product_id,
                    quantityItem=quantity_sold,
                )
                self.session.add(new_item_sale)

            self.session.commit()
            return new_sale
        except Exception as e:
            self.session.rollback()  # Reverte alterações em caso de erro
            raise ValueError(f'Erro ao criar a venda: {str(e)}')

    def get_sale_by_id(self, sale_id: int) -> Sale:
        """
        Recupera uma venda pelo ID.
        :param sale_id: ID da venda.
        :return: Instância de Sale.
        :raises: NoResultFound se a venda não for encontrada.
        """
        sale = self.session.query(Sale).filter_by(sale_id=sale_id).one()
        return sale

    def update_sale(self, sale_id: int, total_sale: float = None) -> Sale:
        """
        Atualiza uma venda existente.
        :param sale_id: ID da venda.
        :param total_sale: Novo total da venda (opcional).
        :return: Venda atualizada.
        :raises: NoResultFound se a venda não for encontrada.
        """
        sale = self.get_sale_by_id(sale_id)

        if total_sale is not None:
            sale.total_sale = total_sale

        self.session.commit()
        return sale

    def delete_sale(self, sale_id: int) -> None:
        """
        Deleta uma venda pelo ID.
        :param sale_id: ID da venda.
        :raises: NoResultFound se a venda não for encontrada.
        """
        sale = self.get_sale_by_id(sale_id)
        self.session.delete(sale)
        self.session.commit()

    def delete_all_sales(self) -> None:
        """
        Deleta todas as vendas da tabela Sale.
        :raises: Exception se ocorrer algum erro durante a exclusão.
        """
        try:
            # Deleta todos os registros da tabela Sale
            self.session.query(Sale).delete()
            self.session.commit()
            print('Todas as vendas foram deletadas com sucesso.')
        except Exception as e:
            self.session.rollback()
            print(f'Erro ao deletar todas as vendas: {e}')

    def list_sales(self) -> list[Sale]:
        """
        Lista todas as vendas no banco de dados.
        :return: Lista de instâncias de Sale.
        """
        sales = self.session.query(Sale).all()
        return sales

    def process_sale(self, total_sale: float, item_sales: list[dict]) -> Sale:
        """
        Processa uma nova venda, ajustando o estoque para os itens vendidos.
        :param total_sale: Total da venda.
        :param item_sales: Lista de dicionários contendo as informações dos itens de venda (product_id, quantityItem).
        :return: A venda criada.
        :raises: ValueError se houver erro no estoque.
        """
        # Ajustar o estoque para cada item vendido
        for item in item_sales:
            product_id = item['product_id']
            quantity_sold = item['quantityItem']

            # Chama o método do StorageController para remover os produtos vendidos
            self.storage_controller.remove_sold_products(
                product_id=product_id, quantity_sold=quantity_sold
            )

        # Após ajustar o estoque, cria a venda
        sale = self.create_sale(total_sale=total_sale, item_sales=item_sales)
        return sale
