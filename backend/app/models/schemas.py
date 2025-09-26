# backend/app/models/schemas.py

from pydantic import BaseModel, HttpUrl
from typing import Optional

class Product(BaseModel):
    id: str
    source: str = "naver"
    title: str
    brand: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = "KRW"
    category_std: Optional[str] = None
    color_std: Optional[str] = None
    size_std: Optional[str] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    in_stock: Optional[bool] = True