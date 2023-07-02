import pickle
from os.path import exists

from utils.fernet import encrypt_and_save, load_and_decrypt
from utils.password import password


class ClassPersist:
    @staticmethod
    def load(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        try:
            obj = pickle.loads(load_and_decrypt(name + '.pkl', password))
            return obj
        except FileNotFoundError:
            return cls

    @staticmethod
    def save(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        data = pickle.dumps(cls, protocol=pickle.HIGHEST_PROTOCOL)
        encrypt_and_save(name + '.pkl', data, password)
