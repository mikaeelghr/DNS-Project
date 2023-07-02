from __future__ import annotations

import base64
import typing

import rsa

from rsa import PublicKey, PrivateKey
from utils.singleton_class import ClassPersist


class KeyManagement:
    def __init__(self, username):
        self.username = username
        self.public_keys: typing.Dict[str, PublicKey] = dict()
        self.my_key: typing.Tuple[PublicKey | None, PrivateKey | None] = None, None

    def generate_key(self):
        public_key, private_key = rsa.newkeys(512)
        self.store_public_key(self.username, public_key)
        self.my_key = public_key, private_key
        ClassPersist.save(self, self.username + '_key')

    def store_public_key(self, username: str, public_key: PublicKey):
        self.public_keys[username] = public_key
        ClassPersist.save(self, self.username + '_key')

    def get_public_key(self, username: str) -> PublicKey:
        return self.public_keys[username]

    def load_my_key(self) -> typing.Tuple[PublicKey, PrivateKey]:
        if self.my_key[0] is None:
            loaded = ClassPersist.load(self, self.username + '_key')
            self.my_key = loaded.my_key
            self.public_keys = loaded.public_keys

        return self.my_key

    @staticmethod
    def public_key_to_str(public_key: PublicKey) -> str:
        return str(base64.b64encode(public_key.save_pkcs1(format='PEM')))[2:-1]

    @staticmethod
    def str_to_public_key(public_key: str) -> PublicKey:
        x = base64.b64decode(public_key)
        return rsa.PublicKey.load_pkcs1(x, format='PEM')

    def get_my_public_key_str(self) -> str:
        pub, _ = self.load_my_key()
        return KeyManagement.public_key_to_str(pub)
