#!pip install cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        salt = os.urandom(16)
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = kdf.derive(self.key)

        cipher = Cipher(algorithms.AES(key), modes.CBC(salt), backend=backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return salt + encrypted_data

    def decrypt(self, cipher_text):
        salt = cipher_text[:16]
        cipher_text = cipher_text[16:]

        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = kdf.derive(self.key)

        cipher = Cipher(algorithms.AES(key), modes.CBC(salt), backend=backend)
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode()
