import pymongo


class AuctionModel:
    def __init__(self):
        pass

    def db_connect(self, col_name):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection["Auct_DB"]
        collection = db[col_name]
        return collection

    def User_req(self):
        collection = self.db_connect("User_req")
        return collection

    def item_Price(self):
        collection = self.db_connect("Items_Prices")
        return collection

    def Bidder(self):
        collection = self.db_connect("Bidders")
        return collection
