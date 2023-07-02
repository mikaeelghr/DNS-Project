from utils.key_manager import KeyManagement
from utils.singleton_class import ClassPersist

manager = ClassPersist.load(KeyManagement("server"), 'server_key')
if manager is None:
    manager = KeyManagement("server")
manager.generate_key()

print(manager.load_my_key())
