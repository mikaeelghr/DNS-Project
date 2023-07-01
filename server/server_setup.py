from utils.key_manager import KeyManagement
from utils.singleton_class import ClassPersist

manager = ClassPersist.load(KeyManagement())
manager.generate_key(0)

print(manager.load_my_key())
