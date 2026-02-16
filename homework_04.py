from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from homework_03 import engine, Base, Category, Product

Base.metadata.create_all(engine)

with Session(engine) as session:
    electronics = Category(name='Электроника', description='Гаджеты и устройства.')
    books = Category(name='Книги', description='Печатные книги и электронные книги.')
    clothes = Category(name='Одежда', description='Одежда для мужчин и женщин.')

    session.add_all([electronics, books, clothes])

    p1 = Product(name='Смартфон', price=Decimal('299.99'), in_stock=True, category=electronics)
    p2 = Product(name='Ноутбук', price=Decimal('499.99'), in_stock=True, category=electronics)
    p3 = Product(name='Научно-фантастический роман', price=Decimal('15.99'), in_stock=True, category=books)
    p4 = Product(name='Джинсы', price=Decimal('40.50'), in_stock=True, category=clothes)
    p5 = Product(name='Футболка', price=Decimal('20.00'), in_stock=True, category=clothes)

    session.add_all([p1, p2, p3, p4, p5])

    session.commit()

    stmt = select(Category)
    categories = session.execute(stmt).scalars().all()

    for category in categories:
        print(category.name)

        for product in category.products:
            print(product.name, product.price)

    stmt = (
        select(Product)
        .where(Product.name == "Смартфон")
    )

    smartphone = session.scalars(stmt).first()

    if smartphone:
        smartphone.price = Decimal('349.99')

        session.commit()

    stmt = (
        select(Product)
        .where(Product.name == "Смартфон")
    )

    smartphone = session.scalars(stmt).first()
    print(f"New price: {smartphone.price}")

    stmt = (
        select(Category.name, func.count(Product.id))
        .join(Product)
        .group_by(Category.id)
    )

    result = session.execute(stmt).all()

    for name, count in result:
        print(f"Category: {name}  |  Count of products: {count}")


    stmt = (
        select(
            Category.name
        )
        .join(Product)
        .group_by(Category.id)
        .having(func.count(Product.id) > 1)
    )

    names = session.scalars(stmt).all()

    for name in names:
        print(f"Category with more the one product: {name}")
