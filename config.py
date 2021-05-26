import os

def load_key():
    '''load key from secret_key.txt'''
    return open("secret_key.txt", "rb").read()
    

class Config(object):
    '''secret key for POST communication with server and controller'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
