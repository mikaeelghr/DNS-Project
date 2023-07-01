import pickle
from utils.fernet import encrypt, decrypt
from utils.password import password

class ClassPersist:
    @staticmethod
    def load(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        try:
            with open(name + '.pkl', 'rb') as inp:
                obj = pickle.load(inp)
            encrypt(name + '.pkl', password)
            return obj
        except FileNotFoundError:
            return cls

    @staticmethod
    def save(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        decrypt(name + '.pkl', password)
        with open(name + '.pkl', 'wb') as handle:
            pickle.dump(cls, handle, protocol=pickle.HIGHEST_PROTOCOL)
