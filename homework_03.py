from sqlalchemy import (
    create_engine,
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
    relationship
)

from decimal import Decimal


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255)
    )

    products = relationship(
        'Product',
        back_populates='category'
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        BigInteger,
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
        Boolean
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('categories.id')
    )

    category = relationship(
        'Category',
        back_populates='products'
    )


Base.metadata.create_all(bind=engine)

print("ALL TABLES ARE CREATED")
print(Base.metadata.tables)
