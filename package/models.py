import sqlalchemy as sq
from sqlalchemy import Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = 'publisher'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sq.String(200), unique=True, nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sq.String(100), nullable=False)
    id_publisher: Mapped[int] = mapped_column(sq.ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)

    publisher: Mapped['Publisher'] = relationship(back_populates='books')


class Shop(Base):
    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sq.String(100), unique=True, nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(sq.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop: Mapped[int] = mapped_column(sq.ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(sq.CheckConstraint('count >= 0', name='check_count'), nullable=False)

    book: Mapped['Book'] = relationship(back_populates='stocks')
    shop: Mapped['Shop'] = relationship(back_populates='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(sq.CheckConstraint('price >= 0', name='check_price'), nullable=False)
    date_sale: Mapped[Date] = mapped_column(default=func.strftime('%d-%m-%Y', func.current_date()))
    id_stock: Mapped[int] = mapped_column(sq.ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(sq.CheckConstraint('count >= 0', name='check_count'), nullable=False)

    stock: Mapped['Stock'] = relationship(back_populates='sale')


def create_tables(engine):
    Base.metadata.create_all(engine)
