from fastapi import FastAPI, HTTPException, Depends, status
from typing import Union

## Database imports:
from sqlalchemy.orm import Session
from data.database import SessionLocal, engine
from data.models import Food
from data import models

## Queries
from pydantic import BaseModel

## Authentification
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from fake_user_data import fake_users_db

class User(BaseModel):
    username: str
    email : Union[str, None] = None
    full_name : Union[str, None] = None
    disabled : Union[bool, None] = None

def fake_decode_token(token):
    return User(username=token+"fakedecoded", email="john@example.com", full_name="John Doe")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

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


## Get current user:
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"acces_token" : user.username, "token_type": "bearer"}




## Endpoints
# Root
@app.get("/")
def get_root_data():
    return {"message": "root"}

@app.get("/food/foodlist")
def get_root_data(token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
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