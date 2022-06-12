from fastapi import FastAPI, HTTPException, Depends

## Database imports:
from sqlalchemy.orm import Session
from data.database import SessionLocal, engine
from data.models import Food
from data import models

## Queries
from pydantic import BaseModel


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class FoodRequest(BaseModel):     
    name: str
    category: str  
    kcal: float
    carbs: float
    protein: float
    fat: float

## Get Instance of Database_
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


## Adding new Foods:
@app.post("/food/newFood")
def add_new_food(food: FoodRequest, db: Session = Depends(get_db)):
    new_food = Food()
    new_food.name = food.name
    new_food.category = food.category
    new_food.kcal = food.kcal
    new_food.carbs = food.carbs
    new_food.protein = food.protein
    new_food.fat = food.fat

    db.add(new_food)
    db.commit()

    return {"message": "ok"}






## Endpoints
# Root
@app.get("/")
def get_root_data():
    return {"message": "root"}

@app.get("/food/foodlist")
def get_root_data(db: Session = Depends(get_db)):
    test = db.query(Food).all()
    return test


# @app.get("/food/list")
# def get_food_list():
#     return foodlist


# @app.get("/food/{name}")
# def get_food_by_name(name:str):
#     for food in foodlist:
#         if food["name"] == name:
#             return food
#     raise HTTPException(status_code=404, detail="food not found")