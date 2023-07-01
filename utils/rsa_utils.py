import json

import rsa
from rsa import VerificationError, common

from utils.key_manager import KeyManagement
from utils.singleton_class import ClassPersist


class RSAUtil:
    def __init__(self, name):
        self.key_manager: KeyManagement = ClassPersist.load(KeyManagement(name), name + '_key')

    def sign(self, message: bytes) -> bytes:
        _, private_key = self.key_manager.load_my_key()
        signature = rsa.sign(message, private_key, 'SHA-512')
        return signature

    def verify(self, username: str, content: bytes, sig: bytes) -> bool:
        key = self.key_manager.get_public_key(username)
        try:
            rsa.verify(content, sig, key)
            return True
        except VerificationError:
            return False

    def encrypt(self, username: str, message: str) -> str:
        public_key = self.key_manager.get_public_key(username)
        result = []
        for n in range(0, len(message), 53):
            part = message[n:n + 53]
            result.append(rsa.encrypt(bytes(part.encode('utf-8')), public_key).hex())
        return ''.join(result)
    
    def encrypt(self, public_key, message: str, flag) -> str:
        result = []
        for n in range(0, len(message), 53):
            part = message[n:n + 53]
            result.append(rsa.encrypt(bytes(part.encode('utf-8')), public_key).hex())
        return ''.join(result)

    def decrypt(self, message: str) -> str:
        _, private_key = self.key_manager.load_my_key()
        bts = bytes.fromhex(message)
        result = []
        for n in range(0, len(bts), 64):
            part = bts[n:n + 64]
            result.append(rsa.decrypt(part, private_key).decode('utf-8'))
        return ''.join(result)
