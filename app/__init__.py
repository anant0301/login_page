from flask import Flask
from flask_login import LoginManager
from config import Config, load_key

# load key
key = load_key()

# make the flask app and add configurations 
app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

# connect to the mongo database 
import pymongo
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')

# database name
db_name = 'day9'

# collections of interest in the database
coll_name = [
    'empl',
    'dept',
    'user'
]

# data types of data headers
coll_constr = {
    'empl': (int, str, int, int, int, int, int),
    'dept': (int, str, int),
    'user': (str, str, bytes)
}

# mongo database object
db = mongo_client[db_name]

# session manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# user headers in the database
user_header = [
    '_id',
    'Email',
    'Password'
]

# employee headers in the database
emp_header = [
    '_id',
    'Employee Name',
    'Salary',
    'HRA',
    'DA',
    'Deductions',
    'Department ID'
]

# department headers in the database
dept_header = [
    '_id',
    'Department Name',
    'Manager ID'
]

from . import routes