from fastapi import FastAPI, HTTPException


app = FastAPI()

foodlist = [
    {"name": "food"},
    {"name": "food1"},
    {"name": "food2"},
    {"name": "food3"},
    {"name": "food4"},
    {"name": "food5"},
    {"name": "food6"},
    {"name": "food7"},
]

# Root
@app.get("/")
def get_root_data():
    return {"message": "root"}


@app.get("/food/list")
def get_food_list():
    return foodlist


@app.get("/food/{name}")
def get_food_by_name(name:str):
    for food in foodlist:
        if food["name"] == name:
            return food
    raise HTTPException(status_code=404, detail="food not found")