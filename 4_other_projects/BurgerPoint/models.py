from pydantic import BaseModel

class Burger(BaseModel): 
    id: int
    name: str
    description: str
    price: int
    category: str
    is_available: bool

class BurgerResponse(BaseModel): 
    status: str = "success"
    count: int
    items: list[Burger]