import os

def load_key():
    return open("secret_key.txt", "rb").read()
    

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    # MONGOALCHEMY_DATABASE = os.environ.get('MONGOALCHEMY_DATABASE') or \
    #     "mongodb://127.0.0.1:27017/"
