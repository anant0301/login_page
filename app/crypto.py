import hashlib
from cryptography.fernet import Fernet
def encrypt(message, key):
    '''encode message based on key passed'''
    encoded_message = message.encode()
    fkey = Fernet(key)
    hashlib.sha256
    return hashlib.sha256(encoded_message).hexdigest()

def decrypt(encrypted, key):
    '''decode message based on key passed'''
    fkey = Fernet(key)
    decrypted_message = fkey.decrypt(encrypted)
    return decrypted_message.decode()