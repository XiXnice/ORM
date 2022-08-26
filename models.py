import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

DSN =
engine = sqlalchemy.create_engine(DSN)


class Publisher(Base):
    __tablename__ = "publisher"

    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False, unique=True)

    def __str__(self):
        return f'Publisher {self.id} : {self.name}'

class Book(Base):
    __tablename__ = "book"

    id_book = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publisher.id_publisher"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'Book {self.id_book} : ({self.title}, {self.id_publisher})'



class Shop(Base):
    __tablename__ = "shop"

    id_shop = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)

    def __str__(self):
        return f'Shop {self.id_shop} : ({self.name})'



class Stock(Base):
    __tablename__ = "stock"

    id_stock = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shop.id_shop"), nullable=False)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id_book"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'Stock {self.id_stock} : ({self.id_shop}, {self.id_book}, {self.count})'



class Sale(Base):
    __tablename__ = "sale"

    id_sale = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
    date_sale = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id_stock"), nullable=False)

    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f'Sale {self.id_sale} : ({self.price}, {self.date_sale}, {self.count}, {self.id_stock})'

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)
