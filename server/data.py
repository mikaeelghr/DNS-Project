import json
from typing import Dict, List, Any, Tuple

from utils.password_utils import get_hashed_password
from utils.singleton_class import ClassPersist


class User:
    def __init__(self, username: str, hashed_password: bytes, public_key):
        self.username = username
        self.hashed_password = hashed_password
        self.public_key = public_key


class BaseRequestBody:
    message_type: str

    def __init__(self, **kwargs):
        self.message_type = kwargs['type']
        args = json.loads(kwargs['body'])
        for key in args:
            self.__setattr__(key, args[key])


class MessageToUserRequestBody(BaseRequestBody):
    to_username: str
    message: str


class MessageToGroupRequestBody(BaseRequestBody):
    to_group_id: int
    message: str


class RemoveFromGroupRequestBody(BaseRequestBody):
    group_id: int
    username: str


class GetNewMessages(BaseRequestBody):
    pass


class Data:
    users: Dict[str, User] = dict()
    messages: Dict[str, List[Tuple[str, int | None, str, str]]] = dict()
    groups: Dict[int, List[str]] = dict()

    @staticmethod
    def load():
        x = ClassPersist.load(Data(), 'server_data')
        Data.users = x.users
        Data.messages = x.messages
        Data.groups = x.groups

    @staticmethod
    def get_new_messages(username: str):
        if username not in Data.messages:
            return []
        messages, Data.messages[username] = Data.messages[username], []
        ClassPersist.save(Data, 'server_data')
        return messages

    @staticmethod
    def send_message_to_user(username: str, body: MessageToUserRequestBody):
        if body.to_username not in Data.messages:
            Data.messages[body.to_username] = []
        Data.messages[body.to_username].append((username, None, body.message_type, body.message))
        ClassPersist.save(Data, 'server_data')

    @staticmethod
    def send_message_to_group(username: str, body: MessageToGroupRequestBody):
        for to_username in Data.groups[body.to_group_id]:
            Data.messages[to_username].append((username, body.to_group_id, body.message_type, body.message))
        ClassPersist.save(Data, 'server_data')

    @staticmethod
    def remove_user_from_group(body: RemoveFromGroupRequestBody):
        Data.groups[body.group_id].remove(body.username)
        ClassPersist.save(Data, 'server_data')

    @staticmethod
    def save_user(username, password, public_key):
        hashed_password = get_hashed_password(password)
        user = User(username, hashed_password, public_key)
        Data.users[username] = user
        ClassPersist.save(Data, 'server_data')


Data.load()


class RegisterRequestBody:
    username: int
    password: int
    public_key: str

    def __init__(self, username, public_key):
        self.username = username
        self.public_key = public_key


class RequestBody:
    username: str
    path_body_sign: str
    body: str

    def __init__(self, username, path, body, path_body_sign):
        self.username = username
        self.path = path
        self.body = body
        self.path_body_sign = path_body_sign

    def get_path_body(self):
        return self.path + ':' + self.body

    def get_body(self):
        if self.path == '/group/send':
            return MessageToGroupRequestBody(**json.loads(self.body))
        elif self.path == '/user/send':
            return MessageToUserRequestBody(**json.loads(self.body))
        elif self.path == '/user/remove':
            return RemoveFromGroupRequestBody(**json.loads(self.body))
        elif self.path == '/messages':
            return GetNewMessages(**json.loads(self.body))
