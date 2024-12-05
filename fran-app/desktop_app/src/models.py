# Este arquivo contém as classes que modelam as regras de negócios
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry

# Registro para mapear as tabelas
table_registry = registry()


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'product'
    product_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]


@table_registry.mapped_as_dataclass
class Storage:
    __tablename__ = 'storage'
    entry_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.product_id'))
    quantity: Mapped[int]
    datetime: Mapped[str] = mapped_column(init=False, default=current_time)
    cost: Mapped[float]


@table_registry.mapped_as_dataclass
class Sale:
    __tablename__ = 'sale'
    sale_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datetime: Mapped[str] = mapped_column(init=False, default=current_time)
    total_sale: Mapped[float]


@table_registry.mapped_as_dataclass
class ItemSale:
    __tablename__ = 'itemsale'
    itemsale_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey('sale.sale_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.product_id'))
    quantityItem: Mapped[int]
