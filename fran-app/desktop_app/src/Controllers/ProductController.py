from sqlalchemy.orm import Session

from models import Product


class ProductController:
    def __init__(self, session: Session):
        """
        Inicializa o controlador com uma sessão SQLAlchemy.
        :param session: Instância de Session do SQLAlchemy.
        """
        self.session = session

    def create_product(
        self, name: str, description: str, price: float
    ) -> Product:
        """
        Cria um novo produto no banco de dados.
        :param name: Nome do produto.
        :param description: Descrição do produto.
        :param price: Preço do produto.
        :return: O produto criado.
        """
        if not name or not description or price is None or price <= 0:
            raise ValueError(
                'Todos os campos obrigatórios devem ser preenchidos corretamente.'
            )

        new_product = Product(name=name, description=description, price=price)
        self.session.add(new_product)
        self.session.commit()
        return new_product

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Recupera um produto pelo ID.
        :param product_id: ID do produto.
        :return: Instância de Product.
        :raises: NoResultFound se o produto não for encontrado.
        """
        product = (
            self.session.query(Product).filter_by(product_id=product_id).one()
        )
        return product

    def update_product(
        self,
        product_id: int,
        name: str = None,
        description: str = None,
        price: float = None,
    ) -> Product:
        """
        Atualiza um produto existente.
        :param product_id: ID do produto.
        :param name: Novo nome (opcional).
        :param description: Nova descrição (opcional).
        :param price: Novo preço (opcional).
        :return: Produto atualizado.
        :raises: NoResultFound se o produto não for encontrado.
        """
        if not name or not description or price is None or price <= 0:
            raise ValueError(
                'Todos os campos obrigatórios devem ser preenchidos corretamente.'
            )

        product = self.get_product_by_id(product_id)

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price

        self.session.commit()
        return product

    def delete_product(self, product_id: int) -> None:
        """
        Deleta um produto pelo ID.
        :param product_id: ID do produto.
        :raises: NoResultFound se o produto não for encontrado.
        """
        product = self.get_product_by_id(product_id)
        self.session.delete(product)
        self.session.commit()

    def delete_all_products(self) -> None:
        """
        Deleta todos os produtos da tabela Product.
        :raises: Exception se ocorrer algum erro durante a exclusão.
        """
        try:
            # Deleta todos os registros da tabela Product
            self.session.query(Product).delete()
            self.session.commit()
            print('Todos os produtos foram deletados com sucesso.')
        except Exception as e:
            self.session.rollback()
            print(f'Erro ao deletar todos os produtos: {e}')

    def list_products(self) -> list[Product]:
        """
        Lista todos os produtos no banco de dados.
        :return: Lista de instâncias de Product.
        """
        products = self.session.query(Product).all()
        return [
            {
                'id': product.product_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
            }
            for product in products
        ]
