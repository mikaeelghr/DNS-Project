import rsa
from rsa import VerificationError

from utils.key_manager import KeyManagement
from utils.singleton_class import ClassPersist


class RSAUtil:
    def __init__(self):
        self.key_manager = ClassPersist.load(KeyManagement)

    def sign(self, message: bytes) -> bytes:
        _, private_key = self.key_manager.load_my_key()
        signature = rsa.sign(message, private_key, 'SHA-512')
        return signature

    def verify(self, user_id: int, content: bytes, sig: bytes) -> bool:
        key = self.key_manager.get_public_key(user_id)
        try:
            rsa.verify(content, sig, key)
            return True
        except VerificationError:
            return False

    def encrypt(self, user_id: int, message: bytes) -> bytes:
        public_key = self.key_manager.get_public_key(user_id)
        return rsa.encrypt(message, public_key)

    def decrypt(self, message: bytes) -> bytes:
        _, private_key = self.key_manager.load_my_key()
        return rsa.decrypt(message, private_key)
