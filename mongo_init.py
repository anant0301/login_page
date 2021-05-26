import pymongo
import json
import pandas as pd

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

db_name = "day9"

coll_name = [
    "empl",
    "dept",
    "user"
]

mongo_client.drop_database(db_name)
db = mongo_client[db_name]

empl_data, dept_data = './app/database/employee.csv', './app/database/department.csv'
df_empl = pd.read_csv(empl_data)
empl_records = json.loads(df_empl.T.to_json()).values()
df_dept = pd.read_csv(dept_data)
dept_records = json.loads(df_dept.T.to_json()).values()
# df_user = pd.read_csv('user.csv')
# user_records = json.loads(df_user.T.to_json()).values()


empl_coll = db[coll_name[0]]
empl_coll.insert(empl_records)
dept_coll = db[coll_name[1]]
dept_coll.insert(dept_records)
# db[coll_name[2]].insert_many(user_records)


mongo_client.close()