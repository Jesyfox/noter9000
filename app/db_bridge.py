import pymongo as pm


class DataBaseHandler:

    def __init__(self, **kwargs):
        self.data_base = None
        self.collection = None
        self.client = pm.MongoClient(kwargs['host'],
                                     kwargs['port'],
                                     connect=False)
        self.make_data_base(kwargs['db_name'])
        self.make_collection(kwargs['col_name'])

    def make_data_base(self, db_name):
        self.data_base = self.client[db_name]

    def make_collection(self, collection_name):
        self.collection = self.data_base[collection_name]

    def new_note(self, note: dict):
        self.collection.insert_one(note)

    def get_notes(self):
        return self.collection.find()





# def new_note(note, db=note_collection):
#     db.insert_one(note)
#
#
# def get_notes(db=note_collection):
#     return db.find()