import pymongo

connection = pymongo.MongoClient("localhost", 27017)
Auction_server = connection["Auct_DB"]
Items_Prices = Auction_server["Items_Prices"]
User_req = Auction_server["User_req"]


class Ob:
    def __init__(self):
        print("Starting OB Program!")

    def get_received(self, data):
        print("OB Received: ", data)
        return data

    def send_data(self, data):
        print("OB Sent:", data)

        return data
