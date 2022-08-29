import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Publisher, Books, Shops, Stocks, Sales, create_tables, drop_tables, dsn
import json

Base = declarative_base()

DSN, engine = dsn()

Session = sessionmaker(bind = engine)
session = Session()

def add_json():
    with open('tests_data.json', 'r', encoding = 'utf-8') as f:
        texts = json.load(f)
        for text in texts:
            if str(text['model']) == 'publisher':
                pu = Publisher(name = text['fields']['name'])
                session.add(pu)
                session.commit()
            elif text['model'] == 'book':
                bo = Books(title = text['fields']['title'], id_publisher = text['fields']['id_publisher'])
                session.add(bo)
                session.commit()
            elif text['model'] == 'shop':
                sh = Shops(name = text['fields']['name'])
                session.add(sh)
                session.commit()
            elif text['model'] == 'stock':
                st = Stocks(id_shop = text['fields']['id_shop'], id_book = text['fields']['id_book'], count = text['fields']['count'])
                session.add(st)
                session.commit()
            elif text['model'] == 'sale':
                sa = Sales(price = text['fields']['price'], date_sale = text['fields']['date_sale'], count = text['fields']['count'], id_stock = text['fields']['id_stock'])
                session.add(sa)
                session.commit()
            else:
                print('Ошибка')

        print('Complete')

def searching_publisher():
    command = int(input('(1)Ввести имя\n(2)Ввести индентификатор\nВведите комманду: '))
    if command == 1:
        query_publisher_name = input('Введите имя (name) издателя: ')
        for i in session.query(Publisher).join(Books.publisher).join(Stocks.books).join(Shops.stocks).all():
            query_result = i.filter(Shops.name.filter(Publisher.name.like(f'%{query_publisher_name}%')))
            for result in query_result.all():
                print(result.name)
    elif command == 2:
        query_publisher_id= input('Введите идентификатор (id) издателя: ')
        for i in session.query(Publisher).join(Books.publisher).join(Stocks.books).join(Shops.stocks).all():
            query_result = i.filter(Shops.name.filter(Publisher.id_publisher == query_publisher_id))
            for result in query_result.all():
                print(result.name)
    else:
        print('Ошибка комманды!')

if __name__ == '__main__':
    # drop_tables(engine)
    # create_tables(engine)
    add_json()
    searching_publisher()

session.close()
