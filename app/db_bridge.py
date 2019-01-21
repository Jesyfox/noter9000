import pymongo as pm


class DataBaseHandler:

    def __init__(self, **kwargs):
        self.data_base = None
        self.collection = None
        self.client = pm.MongoClient(kwargs['host'],
                                     kwargs['port'])
        self.make_data_base(kwargs['db_name'])
        self.make_collection(kwargs['col_name'])

    def make_data_base(self, db_name):
        self.data_base = self.client[db_name]

    def make_collection(self, collection_name):
        self.collection = self.data_base[collection_name]

    def new_note(self, note: dict):
        self.collection.insert_one(note)

    def get_notes(self, sort_by=None, reverse=False):
        if sort_by:
            if reverse:
                sorting = pm.ASCENDING
            else:
                sorting = pm.DESCENDING
            return self.collection.find().sort(sort_by, sorting)
        else:
            return self.collection.find()

    def delete_by_id(self, object_id):
        self.collection.delete_one({'_id': object_id})

    def kill(self):
        self.collection.drop()
