from flask_login import UserMixin
from . import key
from .crypto import decrypt, encrypt

class User(UserMixin):

    def __init__(self, username, password, email= None, encrypt_password= True):
        self.email = email
        self.id = username
        if encrypt_password:
            self.password = password
        else:
            self.__password = password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, username):
        self._id = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = encrypt(password, key)

    def check_password(self, password):
        decrypted = decrypt(self.password, key)
        return decrypted == password
    
    def __eq__(self, user):
        return self.id == user.id and \
            self.email == user.email
