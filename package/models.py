from datetime import date

import sqlalchemy as sq
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = 'publisher'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sq.String(100), unique=True, nullable=False)

    books: Mapped['Book'] = relationship(back_populates='publisher')

    def __str__(self):
        return f'id={self.id}, name={self.name}'


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sq.String(100), nullable=False)
    id_publisher: Mapped[int] = mapped_column(sq.ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)

    publisher: Mapped['Publisher'] = relationship(back_populates='books')
    stock_book: Mapped['Stock'] = relationship(back_populates='book')

    __table_args__ = (sq.UniqueConstraint('title', 'id_publisher', name='title_publisher'),)

    def __str__(self):
        return f'id={self.id}, title={self.title}, id_publisher={self.id_publisher}'


class Shop(Base):
    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sq.String(100), unique=True, nullable=False)

    stock_shop: Mapped['Stock'] = relationship(back_populates='shop')

    def __str__(self):
        return f'id={self.id}, name={self.name}'


class Stock(Base):
    __tablename__ = 'stock'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(sq.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop: Mapped[int] = mapped_column(sq.ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(sq.CheckConstraint('count >= 0', name='check_count'), nullable=False)

    book: Mapped['Book'] = relationship(back_populates='stock_book')
    shop: Mapped['Shop'] = relationship(back_populates='stock_shop')
    sale: Mapped['Sale'] = relationship(back_populates='stock_sale')

    __table_args__ = (sq.UniqueConstraint('id_book', 'id_shop', name='book_shop'),)

    def __str__(self):
        return f'id={self.id}, id_book={self.id_book}, id_shop={self.id_shop}, count={self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(sq.CheckConstraint('price >= 0', name='check_price'), nullable=False)
    date_sale: Mapped[date] = mapped_column(default=func.current_date(), nullable=False)
    id_stock: Mapped[int] = mapped_column(sq.ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(sq.CheckConstraint('count >= 0', name='check_count'), nullable=False)

    stock_sale: Mapped['Stock'] = relationship(back_populates='sale')

    def __str__(self):
        return (f'id={self.id}, price={self.price}, date_sale={self.date_sale},'
                f'id_stock={self.id_stock}, count={self.count}')


def create_tables(engine):
    Base.metadata.create_all(engine)
