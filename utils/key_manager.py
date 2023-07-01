from __future__ import annotations
import typing

import rsa

from rsa import PublicKey, PrivateKey
from utils.singleton_class import ClassPersist


class KeyManagement:
    def __init__(self):
        self.public_keys: typing.Dict[int, PublicKey] = dict()
        self.my_key: typing.Tuple[PublicKey | None, PrivateKey | None] = None, None

    def generate_key(self, my_user_id: int):
        public_key, private_key = rsa.newkeys(512)
        self.store_public_key(my_user_id, public_key)
        self.my_key = public_key, private_key
        ClassPersist.save(self)

    def store_public_key(self, user_id: int, public_key: PublicKey):
        self.public_keys[user_id] = public_key
        ClassPersist.save(self)

    def get_public_key(self, user_id: int) -> PublicKey:
        return self.public_keys[user_id]

    def load_my_key(self) -> typing.Tuple[PublicKey, PrivateKey]:
        return self.my_key
