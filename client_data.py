from utils.key_manager import KeyManagement
from utils.singleton_class import ClassPersist

from typing import Optional, Dict


class ClientData:
    username = 'client'
    groups_secrets: Dict[int, str] = dict()
    chats_secrets: Dict[str, str] = dict()
    key: KeyManagement = KeyManagement(username)

    @staticmethod
    def load(username: Optional[str] = None):
        if username:
            ClientData.username = username
            key.username = username
        ClientData.key.load_my_key()
        x = ClassPersist.load(ClientData(), f'{username}_data')
        ClientData.groups_secrets = x.groups_secrets
        ClientData.chats_secrets = x.chats_secrets

    @staticmethod
    def get_chat_secret(username: str):
        if username not in ClientData.chats_secrets:
            return None
        return ClientData.chats_secrets[username]

    @staticmethod
    def get_group_secret(group_id: int):
        if group_id not in ClientData.groups_secrets:
            return None
        return ClientData.groups_secrets[group_id]
    
    @staticmethod
    def add_chat_secret(username: str, secret: str):
        ClientData.chats_secrets[username] = secret
        ClassPersist.save(ClientData, f'{ClientData.username}_data')
    
    @staticmethod
    def add_group_secret(group_id: int, secret: str):
        ClientData.groups_secrets[group_id] = secret
        ClassPersist.save(ClientData, f'{ClientData.username}_data')

# TODO: load client data after login
ClientData.load()