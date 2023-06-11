import pymongo

connection = pymongo.MongoClient("localhost", 27017)
V_data = connection["v_db"]
collections = V_data["candidates"]

if __name__ == "__main__":
    candidates = [
        {"_id": 1, "name": "James", "v_mark": 0, "v_points": 0, "voter": []},
        {"_id": 2, "name": "John", "v_mark": 0, "v_points": 0, "voter": []},
        {"_id": 3, "name": "Rooney", "v_mark": 0, "v_points": 0, "voter": []},
        {"_id": 4, "name": "Ronaldo", "v_mark": 0, "v_points": 0, "voter": []},
        {"_id": 5, "name": "Messi", "v_mark": 0, "v_points": 0, "voter": []}
    ]

    collections.insert_many(candidates)
