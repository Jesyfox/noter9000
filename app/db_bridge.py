import pymongo as pm
client = pm.MongoClient('mongodb://localhost:27017/')
print('client: ', client)
data_base = client['notes-database']
print('data_base: ', data_base)
note_collection = data_base['note_collection']
print('note_collection', note_collection)


def new_note(note, db=note_collection):
     db.insert_one(note)
#
#
# def get_notes(db=note_collection):
#     return db.find()
