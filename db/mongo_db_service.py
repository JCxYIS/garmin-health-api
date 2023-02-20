import pymongo
from pymongo.server_api import ServerApi


class MongoDbService:
    def __init__(self, connection_string: str):
        self.client = pymongo.MongoClient(connection_string, server_api=ServerApi('1'))
        self.db = self.client['mainDB']
        # print(self.db.list_collections())

    def add_data(self, col: str, data):
        self.db[col].insert_one(data)
