from flask_login import UserMixin

# local file imports
from . import key
from .crypto import decrypt, encrypt

class User(UserMixin):
    '''A user class for session management and user data'''
    '''
    id: protected
    email: public
    password: private
    '''
    def __init__(self, username: str, password: str, email: str= None, encrypt_password: bool= True) -> None:
        ''' Initialize User object
        Args:
            username: str
                user detail: name
            password: str
                user detail: password for login
            email: str= None
                user detail: email in case user forgot password
            encrypt_password: bool= True
                whether the given password is to be encrypted or not
                    True: encrpyt the password
                    False: don't encrpyt the password
        '''
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
        '''return if the given password (not encrypted) and the password stored are equal'''
        decrypted = decrypt(self.password, key)
        return decrypted == password
    
    def __eq__(self, user):
        '''two User objects are equal if they have the same email and username'''
        return self.id == user.id and \
            self.email == user.email
