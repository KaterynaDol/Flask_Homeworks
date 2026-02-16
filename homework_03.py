# Built-in libs firstly
from decimal import Decimal

# 3-rd party libs secondary
from sqlalchemy import (
    create_engine,
    Integer,
    BigInteger,
    String,
    Boolean,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase
)


# local packages, files, classes, functions, constants


class MyBase(DeclarativeBase):
    __abstract__ = True


    # id PK

    # механика по автоопределению __tablename__

    # механика метанастроек моделей для правильного создания имён индексев, ключей, контреинтов

    # сами общие констрейнты

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')

# Session = sessionmaker(bind=engine)
# session = Session()


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    # products = relationship(
    #     'Product',
    #     back_populates='category'
    # )

    products: Mapped[list['Product']] = relationship(back_populates='category')

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )
    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('categories.id')
    )

    # category = relationship(
    #     'Category',
    #     back_populates='products'
    # )

    category: Mapped['Category'] = relationship(back_populates='products')

Base.metadata.create_all(bind=engine)

print("ALL TABLES ARE CREATED")
print(Base.metadata.tables)



