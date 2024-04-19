from tinydb import TinyDB
from image_processing import ProcessedImage

def truncateOrCreateDB(name):
    db = TinyDB(name)
    db.truncate()
    return db

def save_items_to_db(db, items):
    for item in items:
        item_dict = object_to_dict(item)
        db.insert(item_dict)

def object_to_dict(obj):
    obj_dict = {}
    for attr in vars(obj):
        value = getattr(obj, attr)
        obj_dict[attr] = value
    return obj_dict
