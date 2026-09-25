from fastapi import FastAPI, Query, HTTPException

from data import burgers
from models import Burger, BurgerResponse

app = FastAPI()

@app.get("/")
def root(): 
    return {"message": "Welcome to Burger Point"}

@app.get("/burgers")
def get_all_burgers(): 
    return burgers

@app.get("/burgers/search", response_model=BurgerResponse)
def get_burgers_by_categories(category: str | None = Query(default=None)): 
    if category: 
        filtered = [burger for burger in burgers if burger['category'].lower() == category.lower()]
        if not filtered: 
            raise HTTPException(status_code=404, detail="Category does not exist in the Menu")
        return BurgerResponse(count=len(filtered), items=filtered)
    return BurgerResponse(count=len(burgers), items=burgers)

@app.get("/burgers/{id}", response_model=BurgerResponse)
def get_burgers_by_id(id: int): 
    for burger in burgers: 
        if burger['id'] == id: 
            return BurgerResponse(count=1, item=burger)
    raise HTTPException(status_code=404, detail="Item ID does not exist in the menu")
    