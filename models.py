import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def dsn():
    connection_driver = input('Введите драйвер подключения:')
    login = input('Введите логин:')
    password = input('Введите пароль:')
    host = input('Введите хост:')
    name_bd = input('Введите название БД:')

    DSN = f"{connection_driver}://{login}:{password}@localhost:{host}/{name_bd}"
    engine = sqlalchemy.create_engine(DSN)
    return DSN, engine


class Publisher(Base):
    __tablename__ = "publisher"

    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False, unique=True)

    def __str__(self):
        return f'Publisher {self.id} : {self.name}'

class Books(Base):
    __tablename__ = "books"

    id_book = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publisher.id_publisher"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f'Book {self.id_book} : ({self.title}, {self.id_publisher})'



class Shops(Base):
    __tablename__ = "shop"

    id_shop = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)

    def __str__(self):
        return f'Shop {self.id_shop} : ({self.name})'



class Stocks(Base):
    __tablename__ = "stocks"

    id_stock = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shop.id_shop"), nullable=False)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id_book"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    book = relationship(Books, backref="stocks")
    shop = relationship(Shops, backref="stocks")

    def __str__(self):
        return f'Stock {self.id_stock} : ({self.id_shop}, {self.id_book}, {self.count})'



class Sales(Base):
    __tablename__ = "sales"

    id_sale = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
    date_sale = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id_stock"), nullable=False)

    stock = relationship(Stocks, backref="sales")

    def __str__(self):
        return f'Sale {self.id_sale} : ({self.price}, {self.date_sale}, {self.count}, {self.id_stock})'

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)
