from flask import Flask
from flask_login import LoginManager
from config import Config, load_key
from cryptography.fernet import Fernet

key = load_key()

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True
import pymongo

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')

db_name = 'day9'

coll_name = [
    'empl',
    'dept',
    'user'
]

coll_constr = {
    'empl': (int, str, int, int, int, int, int),
    'dept': (int, str, int),
    'user': (str, str, bytes)
}

db = mongo_client[db_name]

app.config['MONGODB_SETTINGS'] = {
    'db': 'day9',
    'host': 'localhost',
    'port': 12345
}

login_manager = LoginManager(app)
login_manager.login_view = 'login'

user_db_header = [
    '_id',
    'Email',
    'Password'
]

emp_header = [
    '_id',
    'Employee Name',
    'Salary',
    'HRA',
    'DA',
    'Deductions',
    'Department ID'
]

dept_header = [
    '_id',
    'Department Name',
    'Manager ID'
]

from . import routes