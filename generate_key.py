from cryptography.fernet import Fernet

def generate_key():
    '''Generate a secret key to store password in particular hash and put into 'secret_key.txt' '''
    with open("./secret_key.txt", "wb+") as key_file:
        key = Fernet.generate_key()
        key_file.write(key)

generate_key()