import json
from typing import Dict, List, Any, Tuple

from utils.password_utils import get_hashed_password
from utils.singleton_class import ClassPersist
from utils.ManageFiles import ManageFiles


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


class MessageToUserLoginRequestBody(BaseRequestBody):
    to_username: str
    message: str


class MessageToGroupRequestBody(BaseRequestBody):
    to_group_id: int
    message: str


class RemoveFromGroupRequestBody(BaseRequestBody):
    group_id: int
    username: str
    admin_username: str


class GetNewMessages(BaseRequestBody):
    pass


class Data:
    users: Dict[str, Tuple[str, str, str]] = dict()
    messages = dict()
    #                   admin-username   state - list of usernames
    groups: Dict[int, Tuple[str, str, List[str]]] = dict()

    @staticmethod
    def load():
        x = ClassPersist.load(None, 'server_data')
        if x is not None:
            Data.users, Data.messages, Data.groups = x

    @staticmethod
    def save():
        ClassPersist.save((Data.users, Data.messages, Data.groups), 'server_data')

    @staticmethod
    def get_new_messages(username: str):
        if username not in Data.messages:
            return []
        messages, Data.messages[username] = Data.messages[username], []
        Data.save()
        return messages

    @staticmethod
    def send_message_to_user(username: str, body: MessageToUserRequestBody):
        if body.to_username not in Data.messages:
            Data.messages[body.to_username] = []
        Data.messages[body.to_username].append((username, None, body.message_type, body.message))
        Data.save()

    @staticmethod
    def send_message_user_login(username: str, body: MessageToUserLoginRequestBody):
        if ManageFiles.user_login(username, body.message):
            Data.messages[body.to_username].append((username, None, body.message_type, "you have successfully"))
        else:
            Data.messages[body.to_username].append((username, None, body.message_type, "the password is not correct"))
        Data.save()

    @staticmethod
    def send_message_to_group(username: str, body: MessageToGroupRequestBody):
        # for to_username in Data.groups[body.to_group_id]:
        for group_id, (body.to_group_id, to_username) in Data.groups.items():
            Data.messages[to_username].append((username, body.to_group_id, body.message_type, body.message))
        Data.save()

    @staticmethod
    def remove_user_from_group(username: str, body: RemoveFromGroupRequestBody):
        admin_username, state, usernames = Data.groups[body.group_id]
        if username == admin_username:
            Data.groups[body.group_id][2].remove(body.username)
        else:
            raise Exception("Sorry, You don't have access to remove users")
        Data.save()

    @staticmethod
    def save_user(username, password, public_key):
        hashed_password = get_hashed_password(password)
        Data.users[username] = (username, hashed_password, public_key)
        Data.save()

Data.load()


class LoginOrRegisterRequestBody:
    username: str
    password: str
    public_key: str

    def __init__(self, username, password, public_key):
        self.username = username
        self.password = password
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
        elif self.path == '/user/login':
            return MessageToUserLoginRequestBody(**json.loads(self.body))
        elif self.path == '/user/remove':
            return RemoveFromGroupRequestBody(**json.loads(self.body))
        elif self.path == '/messages':
            return GetNewMessages(**json.loads(self.body))
