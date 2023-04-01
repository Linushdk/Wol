import pymongo
import config

class mongoDB1:
    def __init__(self, collection):
        self.collection = collection

    def insertOrUpdate(self, document, value):
        if self.collection.find_one(document) is None:
            for d in value:
                document[d] = value[d]
            self.collection.insert_one(document)
        else:
            self.collection.update_one(document, {"$set": value})


def test():
    tickets = mongoDB1(config.DB.tickets)
    tickets.insertOrUpdate({"id": 1}, {"name": "test", "value": 2, "array": [1, 2, 3]})
    test = config.DB.tickets.find_one({"id": 1})
    ids = test["array"]
    for id in ids:
        print(id)
