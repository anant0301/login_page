from pymongo.errors import DuplicateKeyError
from . import *
from .user import User
import pymongo


class Database():
    def __init__(self, db_name, collection_names):
        self.db_name = db_name
        self.collection_names = collection_names
        self.mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.mongo_client[self.db_name]   
        



def update(collection, update_query: dict, key_header, type_constr):
    try:
        db[collection].find_and_modify(
            query= {key_header: type_constr[0](update_query[key_header])},\
            update= {header: type_constr[i](update_query[header]) for i, header in enumerate(list(update_query.keys()))},\
            upsert= True)
    except Exception as err:
        print("Updation Error:", err)


def delete(collection, delete_query: dict):
    return db[collection].remove(delete_query)

def find(collection, find_query: dict, projection: dict= None):
    return db[collection].find(find_query, projection)

def get_key_data(coll_name, key_header):
    data = find(coll_name, {}, {key_header: True})
    keys = []
    for row in data:
        keys.append(row[key_header])
    return keys

def get_table_data(coll_name, headers):
    data = find(coll_name, {}, {header:True for header in headers})
    trans_data = {}
    for row in data:
        trans_data[row[headers[0]]] = [row[d] for d in headers[1:]]
    return trans_data

def add_user(user: User):
    try:
        data_entry = {
            user_db_header[0]: user._id,
            user_db_header[1]: user.email,
            user_db_header[2]: user.password
        }
        db[coll_name[2]].insert(data_entry)
        return True
    except DuplicateKeyError:
        return False

def get_user(id):
    user_data = [x for x in find(coll_name[2], {'_id' : id}, {header: True for header in user_db_header})]
    if len(user_data) == 1:
        user_data = user_data[0]
        return User(username= user_data[user_db_header[0]], email= user_data[user_db_header[1]],\
                password= user_data[user_db_header[2]], encrypt_password= False)
    elif len(user_data) > 1:
        print("Problem in primary key")
    return None