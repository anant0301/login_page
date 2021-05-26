import hashlib
def encrypt(message):
    '''encode message based on key passed'''
    encoded_message = message.encode()
    hashlib.sha256
    return hashlib.sha256(encoded_message).hexdigest()