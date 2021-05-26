from cryptography.fernet import Fernet

def generate_key():
    with open("./secret_key.txt", "wb+") as key_file:
        key = Fernet.generate_key()
        key_file.write(key)

generate_key()