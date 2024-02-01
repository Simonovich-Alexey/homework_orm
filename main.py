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


def info_buy_book(ses, name_publisher):
    if name_publisher.isdigit():
        where = Publisher.id == name_publisher
    else:
        where = Publisher.name.ilike(f'%{name_publisher}%')
    query = (
        select(Book.title,
               Shop.name,
               Sale.price,
               Sale.date_sale,
               Publisher.id,
               )
        .join(Sale.stock_sale)
        .join(Stock.book)
        .join(Stock.shop)
        .join(Book.publisher)
        .group_by(Book.title, Shop.name, Sale.price, Sale.date_sale, Publisher.id)
        .where(where))

    for row in ses.execute(query):
        out = f"{row[0]: <40} | {row[1]: <10} | {row[2]: <8} | {row[3].strftime('%d-%m-%Y')}"
        print(out)


if __name__ == '__main__':

    load_dotenv()
    engine = create_engine(os.getenv('DSN'))
    create_tables(engine)

    name = input("Enter publisher name or ID: ")

    with Session(engine) as session:

        # load_data(session, 'fixtures/tests_data.json')

        info_buy_book(session, name)
