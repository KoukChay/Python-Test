from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

OurData = {}


class Item(BaseModel):
    name: str
    price: float
    brand: str
    Description: str | None = None


app = FastAPI()


@app.get("/get_items")
def get_item():
    return OurData


@app.get("/get_items/{item_name}")
def get_item(item_name: str, q: Union[str, None] = None):
    forBodyRespond: dict = {}
    for key, value in OurData.items():
        if OurData[key]["brand"] == item_name:
            forBodyRespond.update({key: value})
    if len(forBodyRespond) == 0:
        return {"Item": "404-Not Found!"}
    else:
        return forBodyRespond


@app.put("/save_item/{item_id}")
def save_item(item_id: int, item: Item):
    print("data", item)
    new_data = {item_id: item.dict()}
    OurData.update(new_data)
    return OurData
