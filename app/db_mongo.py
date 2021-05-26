from pymongo.errors import DuplicateKeyError
from . import user_header
from .user import User
import pymongo


class Database():
    '''Class for database operations'''
    def __init__(self, db_name: str, collection_names: list):
        '''Initiate connection with the mongo internal server,
        Initialize database variable'''
        self.db_name = db_name
        self.coll_name = collection_names
        self.mongo_client = pymongo.MongoClient()
        self.db = self.mongo_client[self.db_name]
        print('Database Connected')

    def update(self, collection: str, update_query: dict, key_header: str, type_constr: list):
        '''Update/insert the data into the collection
        
        Args:
            collection: str
                collection name
            update_query: dict
                update query of the collections
            key_header: str
                key data record of the collection
            type_constr: list
                constr on the data applied on the update query data
        '''
        try:
            # put constraints on the data and key
            # update/insert (upsert= True) the data in the collection
            self.db[collection].find_and_modify(
                query= {key_header: type_constr[0](update_query[key_header])},\
                update= {header: type_constr[i](update_query[header]) for i, header in enumerate(list(update_query.keys()))},\
                upsert= True)
        except Exception as err:
            print("Updation Error:", err)


    def delete(self, collection: str, delete_query: dict):
        '''delete a record in the collection based on the query
        Args:
            collection: str
                collection name
            delete_query: dict
                deletion query given as input to the pymongo 
        '''
        try:
            self.db[collection].remove(delete_query)
        except Exception as err:
            print("Deletion Error:", err)

    def find(self, collection: str, find_query: dict, projection: dict= None):
        '''find a record based on the query
        
        Args:
            collection: str
                collection name
            query: dict
            project: dict
                =None: Project all
        Return:
            Return cursor for data fetched in query
            else: return empty dict
        '''
        try:
            return self.db[collection].find(find_query, projection)
        except Exception as err:
            print("Find Query Error:", err)
            return dict()

    def get_key_data(self, collection: str, key_header: str) -> list:
        '''return unique value from the key header

        Args:
            collection: str
                collection name
            key_header:
                the unique value header(primary in the SQL context)
        Return:
            keys: list
                values of the key_header type value
        '''
        data = self.find(collection, {}, {key_header: True})
        # trasnform data into list
        keys = []
        for row in data:
            keys.append(row[key_header])
        return keys

    def get_table_data(self, collection: str, headers: str) -> dict:
        '''return unique value from the key header

        Args:
            collection: str
                collection name
            header:
                headers of the collections
        Return:
            trans_data: list
                values in the collection, transofromed into dict with
                {value(header[0]): other_columns(headers[-1])}
        '''
        data = self.find(collection, {}, {header:True for header in headers})
        # trasnform data into required dictionary format
        trans_data = {}
        for row in data:
            trans_data[row[headers[0]]] = [row[d] for d in headers[1:]]
        return trans_data

    def add_user(self, user: User) -> bool:
        '''add user to the user table
        Args:
            user: User
                User object

        Return:
            True: if successful entry
            False: data entry not successful
        '''
        try:
            data_entry = {
                user_header[0]: user._id,
                user_header[1]: user.email,
                user_header[2]: user.password
            }
            self.db[self.coll_name[2]].insert(data_entry)
            return True
        except DuplicateKeyError:
            # when _id value passed is already in the collection
            return False

    def get_user(self, id: str):
        '''get user based on id from the collection
        Args:
            id: str
                username
        Return:
            User(): there exists a user for the requested id
            None: no user exists for the data/ integrity(uniq val) of _id is not there

        '''
        user_data = [x for x in self.find(self.coll_name[2], {'_id' : id}, {header: True for header in user_header})]
        if len(user_data) == 1:
            user_data = user_data[0]
            return User(username= user_data[user_header[0]], email= user_data[user_header[1]],\
                    password= user_data[user_header[2]], encrypt_password= False)
        elif len(user_data) > 1:
            print("Problem in primary key")
        return None

    def __del__(self):
        '''close connection before at destructor call'''
        self.mongo_client.close()