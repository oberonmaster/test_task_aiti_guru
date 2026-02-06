from pydantic import BaseModel, field_serializer
from datetime import datetime
from decimal import Decimal
from typing import List

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: int = None
    
    class Config:
        from_attributes = True

class NomenclatureResponse(BaseModel):
    id: int
    name: str
    quantity: float
    price: float
    category_id: int = None
    
    class Config:
        from_attributes = True
        
    @field_serializer('quantity', 'price')
    def serialize_decimal(self, value: Decimal, _info):
        return float(value)

class ClientResponse(BaseModel):
    id: int
    name: str
    address: str = None
    
    class Config:
        from_attributes = True
        
class ClientCreate(BaseModel):
    name: str
    address: str = None

class OrderResponse(BaseModel):
    id: int
    client_id: int
    order_date: datetime
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    client_id: int
    
class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    nomenclature_id: int
    quantity: float
    price: float
    
    class Config:
        from_attributes = True
        
    @field_serializer('quantity', 'price')
    def serialize_decimal(self, value: Decimal, _info):
        return float(value)
    
class AddToOrderRequest(BaseModel):
    order_id: int
    nomenclature_id: int
    quantity: float
    
    
class TopProductResponse(BaseModel):
    product_name: str
    top_level_category: str
    total_sold: float

class TopProductsResponse(BaseModel):
    products: List[TopProductResponse]
