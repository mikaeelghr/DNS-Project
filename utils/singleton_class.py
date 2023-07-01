import pickle


class ClassPersist:
    @staticmethod
    def load(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        try:
            with open(name + '.pkl', 'rb') as inp:
                obj = pickle.load(inp)
            return obj
        except FileNotFoundError:
            return cls

    @staticmethod
    def save(cls, name=None):
        if name is None:
            name = cls.__class__.__name__
        with open(name + '.pkl', 'wb') as handle:
            pickle.dump(cls, handle, protocol=pickle.HIGHEST_PROTOCOL)
