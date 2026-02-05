"""
Интерфес работы с базой данных
"""


from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Categories, Client, Orders, Nomenclature, OrderItems


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Database:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
    
    # простые CRUD операции
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
    
    def get_session(self):
        return self.Session()
    
    def create_testing_data(self):
        """
        Заполнение базы тестовыми значениями
        """
        # TODO перезаписывать уже имеющиеся данные, если объект с нужным id есть, увеличивая количество
        session = self.get_session()
        
        appliances = Categories(name="Бытовая техника")
        washing_machines = Categories(name="Стиральные машины", parent=appliances)
        refrigerators = Categories(name="Холодильники", parent=appliances)
        single_chamber = Categories(name="Однокамерные", parent=refrigerators)
        dual_chamber = Categories(name="Двухкамерные", parent=refrigerators)
        tv = Categories(name="Телевизоры", parent=appliances)
        
        computers = Categories(name="Компьютеры")
        notebooks = Categories(name="Ноутбуки", parent=computers)
        screen_17_inches = Categories(name="17 дюймов", parent=notebooks)
        screen_19_inches = Categories(name="19 дюймов", parent=notebooks)
        monoblock_computers = Categories(name="Моноблоки", parent=computers)
        
        session.add_all([appliances,
                         washing_machines,
                         refrigerators, single_chamber, dual_chamber,
                         tv,
                         computers,
                         notebooks, screen_17_inches,screen_19_inches,
                         monoblock_computers])
        session.flush()
        
        # Создаем номенклатуру
        product1 = Nomenclature(name="Стиральная машина", quantity=5, price=31999, category_id=washing_machines.id)
        product2 = Nomenclature(name="Однокамерный холодильник", quantity=4, price=21670, category_id=single_chamber.id)
        product3 = Nomenclature(name="Двухкамерный холодильник", quantity=3, price=59990, category_id=dual_chamber.id)
        product4 = Nomenclature(name="Телевизор", quantity=4, price=15263, category_id=tv.id)
        product5 = Nomenclature(name="Ноутбук 14", quantity=5, price=57895, category_id=screen_17_inches.id)
        product6 = Nomenclature(name="Ноутбук 16", quantity=4, price=64693, category_id=screen_19_inches.id)
        product7 = Nomenclature(name="Моноблок", quantity=3, price=32990, category_id=monoblock_computers.id)
        
        session.add_all([product1,
                         product2,
                         product3,
                         product4,
                         product5,
                         product6,
                         product7])
        
        # Создаем клиентов
        client1 = Client(name="Иванов Иван Иванович", address="Адрес 1")
        client2 = Client(name="ООО 'WWW'", address="Адрес 2")
        session.add_all([client1, client2])
        session.flush()
        
        # Создаем заказы
        order1 = Orders(client_id=client1.id)
        order2 = Orders(client_id=client2.id)
        session.add_all([order1, order2])
        session.flush()
        

        
        order_item1 = OrderItems(
            order_id=order1.id,
            nomenclature_id=product1.id,
            quantity=1,
            price=product1.price
        )
        order_item2 = OrderItems(
            order_id=order1.id,
            nomenclature_id=product2.id,
            quantity=2,
            price=product2.price
        )
        order_item3 = OrderItems(
            order_id=order2.id,
            nomenclature_id=product5.id,
            quantity=1,
            price=product5.price
        )
        session.add_all([order_item1, order_item2, order_item3])
        session.flush()
        
        
        product1.quantity -= 1
        product2.quantity -= 2
        product5.quantity -= 1
        
        
        session.commit()
        session.close()
        