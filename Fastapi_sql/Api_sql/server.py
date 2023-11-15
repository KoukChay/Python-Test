from typing import Optional

import MySQLdb

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'toor',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)
dbCursor = conn.cursor()
dbCursor.execute("CREATE DATABASE IF NOT EXISTS moviedb")
dbCursor.execute("USE moviedb")
dbCursor.execute("CREATE TABLE IF NOT EXISTS movielist(id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(30),"
                 "Genre VARCHAR(30), "
                 "Year SMALLINT,Length VARCHAR(30))")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Pydantic model to define the schema of the data
class Item(BaseModel):
    id: Optional[int]
    Name: str
    Genre: str
    Year: int
    Length: str



# Route to create an item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    cursor = conn.cursor()
    query = "INSERT INTO movielist (id,Name,Genre,Year,Length) VALUES (%s,%s, %s,%s, %s)"
    cursor.execute(query, (item.id, item.Name, item.Genre, item.Year, item.Length))
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    return item


# Route to read an item
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    cursor = conn.cursor()
    query = "SELECT id, Name,Genre,Year,Length FROM movielist WHERE id=%s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "Name": item[1], "Genre": item[2], "Year": item[3], "Length": item[4]}


# Route to update an item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    cursor = conn.cursor()
    query = "UPDATE movielist SET Name=%s, Genre=%s, Year=%s, Length=%s WHERE id=%s"
    cursor.execute(query, (item.Name, item.Genre, item.Year, item.Length, item_id))
    conn.commit()
    cursor.close()
    item.id = item_id
    return item


# Route to delete an item
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM movielist WHERE id=%s"
    cursor.execute(query, (item_id,))
    conn.commit()
    cursor.close()
    return {"id": item_id}
