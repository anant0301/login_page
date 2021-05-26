from cryptography.fernet import Fernet
def encrypt(message, key):
    '''encode message based on key passed'''
    encoded_message = message.encode()
    f = Fernet(key)
    return f.encrypt(encoded_message)

def decrypt(encrypted, key):
    '''decode message based on key passed'''
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted)
    return decrypted_message.decode()