from cryptography.fernet import Fernet


def encrypt_and_save(filename, file_data, key):
    f = Fernet(key)
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    
    
def load_and_decrypt(filename, key) -> bytes:
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    return f.decrypt(encrypted_data)
