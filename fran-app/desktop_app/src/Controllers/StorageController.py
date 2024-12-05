from sqlalchemy.orm import Session

from models import Storage


class StorageController:
    def __init__(self, session: Session):
        """
        Inicializa o controlador com uma sessão SQLAlchemy.
        :param session: Instância de Session do SQLAlchemy.
        """
        self.session = session

    def create_registry(
        self, product_id: int, quantity: int, cost: float
    ) -> Storage:
        """
        Cria um novo produto na tabela estoque.
        :param product_id: ID do produto.
        :param quantity: Quantidade inicial do produto.
        :param cost: Preço unitário do produto.
        :return: O registro criado no estoque.
        """
        new_registry = Storage(
            product_id=product_id,
            quantity=quantity,
            cost=cost,
        )
        self.session.add(new_registry)
        self.session.commit()
        return new_registry

    def get_registry_by_id(self, id: int) -> Storage:
        """
        Recupera um produto registrado na tabela estoque pelo ID.
        :param id: ID da entrada no estoque.
        :return: Instância de Storage correspondente.
        """
        storage = (
            self.session.query(Storage).filter_by(product_id=id).one_or_none()
        )
        if not storage:
            raise ValueError(
                f'Registro com ID {id} não encontrado no estoque.'
            )
        return storage

    def update_registry(
        self, product_id: int, quantity: int = None, cost: float = None
    ) -> Storage:
        """
        Atualiza um produto existente na tabela estoque.
        :param product_id: ID do produto.
        :param quantity: Nova quantidade (opcional).
        :param cost: Novo preço unitário (opcional).
        :return: Registro atualizado.
        :raises: ValueError se nenhum dado válido for fornecido ou se o produto não existir.
        """
        storage = (
            self.session.query(Storage)
            .filter_by(product_id=product_id)
            .one_or_none()
        )
        if not storage:
            raise ValueError(
                f'Produto com ID {product_id} não encontrado no estoque.'
            )

        if quantity is not None:
            storage.quantity = quantity
        if cost is not None and cost > 0:
            storage.cost = cost

        self.session.commit()
        return storage

    def delete_registry(self, id: int) -> None:
        """
        Deleta um registro na tabela estoque pelo ID.
        :param id: ID da entrada no estoque.
        :raises: ValueError se o registro não for encontrado.
        """
        storage = self.get_registry_by_id(id)
        self.session.delete(storage)
        self.session.commit()

    def list_storage(self) -> list[dict]:
        """
        Lista todos os registros na tabela estoque.
        :return: Lista de dicionários representando cada registro no estoque.
        """
        storage_list = self.session.query(Storage).all()
        return [
            {
                'entry_id': storage.entry_id,
                'product_id': storage.product_id,
                'quantity': storage.quantity,
                'datetime': storage.datetime,
                'cost': storage.cost,
            }
            for storage in storage_list
        ]

    def remove_sold_products(
        self, product_id: int, quantity_sold: int
    ) -> Storage:
        """
        Remove a quantidade vendida de um produto no estoque.
        :param product_id: ID do produto.
        :param quantity_sold: Quantidade a ser removida.
        :return: Registro atualizado no estoque.
        :raises: ValueError se o estoque for insuficiente ou o produto não existir.
        """
        storage = (
            self.session.query(Storage)
            .filter_by(product_id=product_id)
            .one_or_none()
        )
        if not storage:
            raise ValueError(
                f'Produto com ID {product_id} não encontrado no estoque.'
            )

        if storage.quantity < quantity_sold:
            raise ValueError(
                f'Estoque insuficiente para o produto ID {product_id}. '
                f'Quantidade disponível: {storage.quantity}, solicitada: {quantity_sold}.'
            )

        storage.quantity -= quantity_sold
        self.session.commit()
        return storage

    def get_stock(self, product_id: int) -> int:
        """
        Retorna a quantidade disponível de um produto no estoque.
        :param product_id: ID do produto.
        :return: Quantidade disponível do produto no estoque.
        :raises: ValueError se o produto não for encontrado no estoque.
        """
        storage = (
            self.session.query(Storage)
            .filter_by(product_id=product_id)
            .one_or_none()
        )
        if not storage:
            raise ValueError(
                f'Produto com ID {product_id} não encontrado no estoque.'
            )

        return storage.quantity

    def update_stock(self, product_id: int, quantity: int) -> Storage:
        """
        Atualiza a quantidade de um produto no estoque.
        :param product_id: ID do produto.
        :param quantity: Quantidade a ser adicionada ou subtraída do estoque.
        :return: O registro atualizado no estoque.
        :raises: ValueError se o produto não for encontrado no estoque.
        """
        storage = (
            self.session.query(Storage)
            .filter_by(product_id=product_id)
            .one_or_none()
        )
        if not storage:
            raise ValueError(
                f'Produto com ID {product_id} não encontrado no estoque.'
            )

        # Atualiza a quantidade do produto
        storage.quantity += (
            quantity  # Pode ser negativo para diminuir a quantidade
        )
        if storage.quantity < 0:
            raise ValueError(
                f'Estoque insuficiente para o produto ID {product_id}.'
            )

        self.session.commit()
        return storage

    def delete_all_storage(self) -> None:
        """
        Deleta todos os registros na tabela estoque.
        :raises: Exception se ocorrer algum erro durante a operação.
        """
        try:
            self.session.query(
                Storage
            ).delete()  # Deleta todos os registros da tabela Storage
            self.session.commit()  # Aplica as mudanças
            print('Todos os registros de Storage foram deletados com sucesso!')
        except Exception as e:
            self.session.rollback()  # Desfaz a transação caso haja erro
            print(f'Erro ao deletar todos os registros de Storage: {e}')
