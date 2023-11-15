from fastapi import FastAPI
from typing import Union

app = FastAPI()
myItemList=["weather","raindrop","BPM180","windspeed"]
@app.get("/")
def read_root():
    return {"Data": "This is Data"}

@app.get("/items/{item_id}")
def read_items(item_id : int , q:Union[str,None]=None):
    return {"item_id":item_id, "q":q}

@app.get("/name/{item_name}")
def read_name(item_name : str , q:Union[str,None]=None):
    for i in range(len(myItemList)):
        if item_name == myItemList[i]:
            return {"Your Item": item_name}

    return {"Invalid": item_name}