import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables, drop_tables
import json

Base = declarative_base()

DSN =
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind = engine)
session = Session()

def add_json():
    with open('C:\Project\Lesson\ORM/tests_data.json', 'r', encoding = 'utf-8') as f:
        texts = json.load(f)
        for text in texts:
            if str(text['model']) == 'publisher':
                pub = Publisher(name = text['fields']['name'])
                session.add(pub)
                session.commit()
            elif text['model'] == 'book':
                pub = Book(title = text['fields']['title'], id_publisher = text['fields']['id_publisher'])
                session.add(pub)
                session.commit()
            elif text['model'] == 'shop':
                pub = Shop(name = text['fields']['name'])
                session.add(pub)
                session.commit()
            elif text['model'] == 'stock':
                pub = Stock(id_shop = text['fields']['id_shop'], id_book = text['fields']['id_book'], count = text['fields']['count'])
                session.add(pub)
                session.commit()
            elif text['model'] == 'sale':
                pub = Sale(price = text['fields']['price'], date_sale = text['fields']['date_sale'], count = text['fields']['count'], id_stock = text['fields']['id_stock'])
                session.add(pub)
                session.commit()
            else:
                print('Ошибка')

        print('Complete')

def searching_publisher():
    command = int(input('(1)Ввести имя\n(2)Ввести индентификатор\nВведите комманду: '))
    if command == 1:
        query_join = session.query(Publisher)
        query_publisher_name = input('Введите имя (name) издателя: ')
        query_result = query_join.filter(Publisher.name.like(f'%{query_publisher_name}%'))
        for result in query_result.all():
            print(result.name)
    elif command == 2:
        query_join_id = session.query(Publisher)
        query_publisher_id= input('Введите идентификатор (id) издателя: ')
        query_result_id = query_join_id.filter(Publisher.id_publisher == query_publisher_id)
        for result_id in query_result_id.all():
            print(result_id.name)
    else:
        print('Ошибка комманды!')

if __name__ == '__main__':
    # searching_publisher()
    drop_tables(engine)
    create_tables(engine)
    add_json()
    searching_publisher()

session.close()
