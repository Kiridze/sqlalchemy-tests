from datetime import datetime
from random import choice, choices, randint

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        Numeric, SmallInteger, String, Table, create_engine)
from sqlalchemy.orm import (Session, declarative_base, relationship,
                            sessionmaker)

engine = create_engine(f'sqlite:///database.sqlite3')

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

fname = {
    "m": ["Николай","Руслан","Алексей","Юрий","Ярослав","Семен","Евгений","Олег","Артур","Петр","Степан","Вячеслав","Сергей","Василий","Степа","Федор","Стас","Вячеслав","Георгий","Антон","Борис","Захар","Арсений","Виктор","Родион","Святослав","Игорь","Гордей"],
    "w": ["Кристина", "Любовь", "Евдокия", "Калерия", "Рада", "Александра", "Белла", "Ярослава", "Антонина", "Ирина", "Мирослава", "Елизавета", "Софья", "Агата", "Марина", "Устинья", "Элеонора", "Диана", "Алевтина", "Августа", "Эвелина", "Ника", "Зинаида", "София", "Маргарита"]
}

lname = [
    "Смирнов","Иванов","Кузнецов","Соколов","Попов","Лебедев","Козлов","Новиков","Морозов","Петров","Волков","Соловьёв","Васильев","Зайцев","Павлов",
    "Семёнов","Голубев","Виноградов","Богданов","Воробьёв","Фёдоров","Михайлов","Беляев","Тарасов","Белов","Комаров","Орлов","Киселёв","Макаров",
    "Андреев","Ковалёв","Ильин","Гусев","Титов","Кузьмин","Кудрявцев","Баранов","Куликов","Алексеев","Степанов","Яковлев","Сорокин","Сергеев","Романов",
    "Захаров","Борисов","Королёв","Герасимов","Пономарёв","Григорьев","Лазарев","Медведев","Ершов","Никитин","Соболев","Рябов","Поляков","Цветков",
    "Данилов","Жуков","Фролов","Журавлёв","Николаев","Крылов","Максимов","Сидоров","Осипов","Белоусов","Федотов","Дорофеев","Егоров","Матвеев",
    "Бобров","Дмитриев","Калинин","Анисимов","Петухов","Антонов","Тимофеев","Никифоров","Веселов","Филиппов","Марков","Большаков","Суханов","Миронов",
    "Ширяев","Александров","Коновалов","Шестаков","Казаков","Ефимов","Денисов","Громов","Фомин","Давыдов","Мельников","Щербаков","Блинов","Колесников",
    "Карпов","Афанасьев","Власов","Маслов","Исаков","Тихонов","Аксёнов","Гаврилов","Родионов","Котов","Горбунов","Кудряшов","Быков","Зуев","Третьяков",
    "Савельев","Панов","Рыбаков","Суворов","Абрамов","Воронов","Мухин","Архипов","Трофимов","Мартынов","Емельянов","Горшков","Чернов","Овчинников",
    "Селезнёв","Панфилов","Копылов","Михеев","Галкин","Назаров","Лобанов","Лукин","Беляков","Потапов","Некрасов","Хохлов","Жданов","Наумов","Шилов",
    "Воронцов","Ермаков","Дроздов","Игнатьев","Савин","Логинов","Сафонов","Капустин","Кириллов","Моисеев","Елисеев","Кошелев","Костин","Горбачёв","Орехов",
    "Ефремов","Исаев","Евдокимов","Калашников","Кабанов","Носков","Юдин","Кулагин","Лапин","Прохоров","Нестеров","Харитонов","Агафонов","Муравьёв","Ларионов",
    "Федосеев","Зимин","Пахомов","Шубин","Игнатов","Филатов","Крюков","Рогов","Кулаков","Терентьев","Молчанов","Владимиров","Артемьев","Гурьев","Зиновьев","Гришин",
    "Кононов","Дементьев","Ситников","Симонов","Мишин","Фадеев","Комиссаров","Мамонтов","Носов","Гуляев","Шаров","Устинов","Вишняков","Евсеев","Лаврентьев","Брагин",
    "Константинов","Корнилов","Авдеев","Зыков","Бирюков","Шарапов","Никонов","Щукин","Дьячков","Одинцов","Сазонов","Якушев","Красильников","Гордеев","Самойлов",
    "Князев","Беспалов","Уваров","Шашков","Бобылёв","Доронин","Белозёров","Рожков","Самсонов","Мясников","Лихачёв","Буров","Сысоев","Фомичёв","Русаков","Стрелков",
    "Гущин","Тетерин","Колобов","Субботин","Фокин","Блохин","Селиверстов","Пестов","Кондратьев","Силин","Меркушев","Лыткин","Туров"
]

grocery_list = [
    "Яблоки", "Бананы", "Апельсины", "Груши", "Виноград",
    "Мандарины", "Лимоны", "Киви", "Персики", "Сливы",
    "Картофель", "Морковь", "Лук", "Чеснок", "Капуста",
    "Огурцы", "Помидоры", "Перец", "Кабачки", "Баклажаны",
    "Хлеб", "Молоко", "Кефир", "Сметана", "Йогурт",
    "Сыр", "Творог", "Яйца", "Масло сливочное", "Масло растительное",
    "Мука", "Сахар", "Соль", "Рис", "Гречка",
    "Макароны", "Курица", "Говядина", "Свинина", "Рыба",
    "Колбаса", "Сосиски", "Чай", "Кофе", "Какао",
    "Шоколад", "Мёд", "Варенье", "Печенье", "Конфеты"
]


# users = [Customer(first_name=choice(fname["m"]), last_name=choice(lname), username=f"@user_{i}", email=f"user_{i}@gmail.com") for i in range(1, 5)]
# session.add_all(users)

# items = [Item(name=grocery, cost_price=randint(5, 10), selling_price=randint(15, 20), quantity=randint(50, 100)) for grocery in grocery_list]
# session.add_all(items)

# customers = session.query(Customer).all()
# orders = [Order(customer_id=customer.id) for customer in customers]
# session.add_all(orders)

orders = session.query(Order).all()
items = session.query(Item).all()
order_line = [OrderLine(order_id=order.id, item_id=choice(items).id, quantity=randint(1, 5)) for order in orders]
session.add_all(order_line)

session.commit()
