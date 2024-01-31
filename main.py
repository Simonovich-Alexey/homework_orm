import os
import json
from dotenv import load_dotenv
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from package.models import create_tables, Book, Shop, Sale, Publisher, Stock


def load_data(ses, path):
    """
     Загрузка тестовых данных в базу данных
    :param ses: session
    :param path: путь до JSON-файла с данными

    """
    with open(path) as f:
        data = json.load(f)

    for row in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[row.get('model')]
        add_db = model(id=row.get('pk'), **row.get('fields'))
        with ses.begin():
            ses.add(add_db)


def info_buy_book(ses, publisher):
    query = (
        select(Book.title,
               Shop.name,
               Sale.price,
               Sale.date_sale,
               Publisher.id,
               Sale.count
               )
        .join(Sale.stock_sale)
        .join(Stock.book)
        .join(Stock.shop)
        .join(Book.publisher)
        .group_by(Book.title, Shop.name, Sale.price, Sale.date_sale, Publisher.id, Sale.count)
        .where(Publisher.name.ilike(f'%{publisher}%')))

    for row in ses.execute(query):
        out = f"{row[0]} | {row[1]} | {row[2] * row[5]} | {row[3]}"
        print(out)


if __name__ == '__main__':

    load_dotenv()
    engine = create_engine(os.getenv('DSN'))
    create_tables(engine)

    with Session(engine) as session:

        load_data(session, 'fixtures/tests_data.json')

        info_buy_book(session, 'O’Reilly')
