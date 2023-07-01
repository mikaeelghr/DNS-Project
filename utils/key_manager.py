from __future__ import annotations
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
        return self.my_key
