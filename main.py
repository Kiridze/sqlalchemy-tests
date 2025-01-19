from datetime import datetime
from random import choice, choices, randint

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        Numeric, SmallInteger, String, Table, create_engine)
from sqlalchemy.orm import (Session, declarative_base, relationship,
                            sessionmaker)

engine = create_engine(url=f'sqlite:///database.sqlite3', echo=False)

Base = declarative_base()

# session = sessionmaker(bind=engine)
session = Session(bind=engine)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    orders = relationship("Order", backref='customer')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    cost_price =  Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2),  nullable=False)
    quantity = Column(Integer())


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    date_placed = Column(DateTime(), default=datetime.now)
    line_items = relationship("OrderLine", backref='order')


class OrderLine(Base):
    __tablename__ = 'order_lines'
    id =  Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.id'))
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(SmallInteger())
    item = relationship("Item")

Base.metadata.create_all(engine)

c1 = Customer(first_name = 'Dmitriy', last_name = 'Yatsenko', username = 'Moseend', email = 'moseend@mail.com')
c2 = Customer(first_name = 'Valeriy', last_name = 'Golyshkin', username = 'Fortioneaks', email = 'fortioneaks@gmail.com')
c3 = Customer(first_name = "Vadim", last_name = "Moiseenko", username = "Antence73", email = "antence73@mail.com",)
c4 = Customer(first_name = "Vladimir", last_name = "Belousov", username = "Andescols", email = "andescols@mail.com")
c5 = Customer(first_name = "Tatyana", last_name = "Khakimova", username = "Caltin1962", email = "caltin1962@mail.com")
c6 = Customer(first_name = "Pavel", last_name = "Arnautov", username = "Lablen", email = "lablen@mail.com")
# session.add_all([c1, c2, c3, c4, c5, c6])
# print("\n".join([f'{user.id} {user.first_name} {user.last_name}' for user in session.new]))

i1 = Item(name = 'Chair', cost_price = 9.21, selling_price = 10.81, quantity = 5)
i2 = Item(name = 'Pen', cost_price = 3.45, selling_price = 4.51, quantity = 3)
i3 = Item(name = 'Headphone', cost_price = 15.52, selling_price = 16.81, quantity = 50)
i4 = Item(name = 'Travel Bag', cost_price = 20.1, selling_price = 24.21, quantity = 50)
i5 = Item(name = 'Keyboard', cost_price = 20.1, selling_price = 22.11, quantity = 50)
i6 = Item(name = 'Monitor', cost_price = 200.14, selling_price = 212.89, quantity = 50)
i7 = Item(name = 'Watch', cost_price = 100.58, selling_price = 104.41, quantity = 50)
i8 = Item(name = 'Water Bottle', cost_price = 20.89, selling_price = 25, quantity = 50)
# session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])

o1 = Order(customer = c1)
o2 = Order(customer = c1)

line_item1 = OrderLine(order = o1, item = i1, quantity =  3)
line_item2 = OrderLine(order = o1, item = i2, quantity =  2)
line_item3 = OrderLine(order = o2, item = i1, quantity =  1)
line_item3 = OrderLine(order = o2, item = i2, quantity =  4)
# session.add_all([o1, o2])

o3 = Order(customer = c1)
orderline1 = OrderLine(item = i1, quantity = 5)
orderline2 = OrderLine(item = i2, quantity = 10)

o3.line_items.append(orderline1)
o3.line_items.append(orderline2)

session.add_all([o3,])

session.commit()
