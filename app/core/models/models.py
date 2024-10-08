from datetime import datetime

from sqlalchemy import (Integer, String, Text, ForeignKey, DECIMAL,
                        DateTime, func, UniqueConstraint, CheckConstraint)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class Product(Base):
    """
    Класс для представления продукта. Содержит поля:
    id, name, description, price, amount_left и связь с OrderItem.
    Обеспечивает уникальность имени и проверку на положительные
    значения цены и количества.
    """

    __tablename__ = 'products'
    __table_args__ = (
        UniqueConstraint('name', name='unique_name'),
        CheckConstraint('price > 0', name='check_price'),
        CheckConstraint('amount_left >= 0', name='check_amount'),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False,
                                      unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    amount_left: Mapped[int] = mapped_column(Integer, nullable=False)

    order_items: Mapped[list['OrderItem']] = relationship(
        'OrderItem', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return (f'<Product(id={self.id}, name="{self.name}",'
                f' price={self.price})>')

    def __str__(self):
        return (f'Product "{self.name}" (ID: {self.id}) - '
                f'Price: {self.price}, Stock: {self.amount_left}')


class Order(Base):
    """
    Класс для представления заказа. Содержит поля:
    id, created_at, status и связь с OrderItem.
    По умолчанию статус - "В процессе", дата создания устанавливается автоматически.
    """

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(
        String(55), nullable=False, default='В процессе')
    order_items: Mapped[list['OrderItem']] = relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')

    def __repr__(self):
        return (f'<Order(id={self.id}, status="{self.status}",'
                f' created_at={self.created_at})>')

    def __str__(self):
        created = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return (f'Order #{self.id} - Status: {self.status}, '
                f'Created at: {created}')


class OrderItem(Base):
    """
    Класс для представления позиции заказа (OrderItem).
    Связывает заказ и продукт, указывая количество продукта в заказе.
    Содержит уникальное ограничение на сочетание order_id и
    product_id для предотвращения дублирования.
    """

    __tablename__ = 'order_items'
    __table_args__ = (
        UniqueConstraint('order_id', 'product_id',
                         name='unique_order_product'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id',  ondelete='CASCADE'))
    amount_of_product: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Order'] = relationship('Order',
                                          back_populates='order_items')
    product: Mapped['Product'] = relationship('Product',
                                              back_populates='order_items')

    def __repr__(self):
        return (f'<OrderItem(id={self.id}, order_id={self.order_id}, '
                f'product_id={self.product_id},'
                f' amount={self.amount_of_products})>')

    def __str__(self):
        product_name = self.product.name
        return (f'OrderItem #{self.id} - Order #{self.order_id}, '
                f'Product: "{product_name}",'
                f' Quantity: {self.amount_of_products}')
