"""Основной скрипт запуска приложения"""

from database.database import Database
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from database.models import Categories, Nomenclature, Client, Orders, OrderItems
from typing import List
from schemas import NomenclatureResponse, ClientResponse, OrderResponse, ClientCreate, OrderCreate, OrderItemResponse, AddToOrderRequest, TopProductResponse
from datetime import datetime


app = FastAPI()

db_instance = Database("testing.db")
def get_db():
    session = db_instance.get_session()
    try:
        yield session
    finally:
        session.close()


@app.get("/categories")
def get_full_tree(db: Session = Depends(get_db)):
    return Categories.get_tree(db)

@app.get("/nomenclature", response_model=List[NomenclatureResponse])
def get_nomenclature(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Nomenclature).offset(skip).limit(limit).all()
    return items

@app.get("/clients", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients

@app.post("/add_client", response_model=ClientResponse)
def add_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(name=client_data.name, address=client_data.address)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
    

@app.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Orders).all()
    return orders

@app.post("/add_order", response_model=OrderResponse)
def add_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    new_order = Orders(client_id=order_data.client_id, order_date=datetime.now())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.post("/add_to_order", response_model=OrderItemResponse)
def add_to_order(request: AddToOrderRequest, db: Session = Depends(get_db)):
    order = db.query(Orders).filter(Orders.id == request.order_id).first()
    if order:
        product = db.query(Nomenclature).filter(Nomenclature.id == request.nomenclature_id).first()
        if product:
            if product.quantity >= request.quantity:
                existing_item = db.query(OrderItems).filter(OrderItems.order_id == request.order_id,OrderItems.nomenclature_id == request.nomenclature_id).first()
                if existing_item:
                    product.quantity -= request.quantity
                    existing_item.quantity += request.quantity
                    db.commit()
                    db.refresh(existing_item)
                    return existing_item
                else:
                    new_item = OrderItems(
                        order_id=request.order_id,
                        nomenclature_id=request.nomenclature_id,
                        quantity=request.quantity,
                        price=product.price
                    )
                    db.add(new_item)
                    db.commit()
                    db.refresh(new_item)
                    return new_item
            else:
                raise HTTPException(status_code=400, detail=f"Недостаточно товара на складе. Доступно: {product.quantity}")
        else:
            raise HTTPException(status_code=404, detail="Товар не найден")
    else:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    

@app.get("/top5", response_model=List[TopProductResponse])
def get_top5query():
    top = db_instance.get_top_5_products()
    return top

def main():
    print("Скрипт запущен")
    print("Инициализация базы")
    db = Database("testing.db")
    # print("Заполнение базы тестовыми значениями")
    # db.create_testing_data()
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
    