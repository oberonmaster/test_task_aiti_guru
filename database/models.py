"""
Модели сущностей БД
"""

from sqlalchemy.orm import DeclarativeBase, Relationship, backref
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Categories(Base):
    """
    Дерево категорий
    """
    __tablename__ = "categories"
    
    # Поля
    id  = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="Наименование категории")
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, comment="Родительская категория")
    
    # Связи
    parent = Relationship("Categories", remote_side=[id],backref=backref("children", cascade="all, delete-orphan"),foreign_keys=[parent_id])
    nomenclature_items = Relationship('Nomenclature', back_populates="category", cascade="all, delete-orphan")
    
    # Методы
    @classmethod
    def get_tree(cls, session, parent_id=None):
        return cls._get_tree_recursive_sql(session, parent_id)    


class Nomenclature(Base):
    """
    Номенклатура
    """
    __tablename__ = "nomenclature"
    
    # Поля
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="Наименование товара")
    quantity = Column(DECIMAL(15, 3), nullable=False, default=0, comment="Количество")
    price = Column(DECIMAL(15, 2), nullable=False, default=0, comment="Стоимость")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, comment="Категория товара")
    
    # Связи
    category = Relationship("Categories", back_populates="nomenclature_items")
    order_items = Relationship("OrderItems", back_populates="nomenclature", cascade="all, delete-orphan")


class Client(Base):
    """
    Клиенты
    """
    __tablename__ = "clients"
    
    # Поля
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="Наименование клиента")
    address = Column(Text, comment="Адрес клиента")
    
    # Связи
    orders = Relationship("Orders", back_populates="client", cascade="all, delete-orphan")


class Orders(Base):
    """
    Заказы
    """
    __tablename__ = "orders"
    
    # Поля
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, comment="Клиент")
    order_date = Column(DateTime, nullable=False, default=datetime.now, comment="Дата создания заказа")
    
    # Связи
    client = Relationship("Client", back_populates="orders")
    order_items = Relationship("OrderItems", back_populates="order", cascade="all, delete-orphan")
    

class OrderItems(Base):
    """
    Товар в заказе
    """
    __tablename__ = 'order_items'
    
    # Поля
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, comment="Заказ")
    nomenclature_id = Column(Integer, ForeignKey('nomenclature.id', ondelete='RESTRICT'), nullable=False, comment="Товар")
    quantity = Column(DECIMAL(15, 3), nullable=False, comment="Количество товара")
    price = Column(DECIMAL(15, 2), nullable=False, comment="Цена на момент заказа")
    
    # Связи
    order = Relationship("Orders", back_populates="order_items")
    nomenclature = Relationship("Nomenclature", back_populates="order_items")
