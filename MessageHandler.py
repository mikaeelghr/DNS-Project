import json
from time import sleep
from typing import List
from enum import Enum

import requests
from client_data import ClientData

from utils.key_manager import KeyManagement
from utils.rsa_utils import RSAUtil
from utils.singleton_class import ClassPersist


class MessageType(Enum):
    # normal message
    NORMAL = 'NORMAL'
    INITIATE_DIFFIE_HELLMAN = 'INITIATE_DIFFIE_HELLMAN'
    SYSTEM_DIFFIE_HELLMAN_STEP2 = 'SYSTEM_DIFFIE_HELLMAN_STEP2'
    USER_REMOVED_FROM_GROUP = 'USER_REMOVED_FROM_GROUP'
    USER_ADDED_TO_GROUP = 'USER_ADDED_TO_GROUP'

    REQUEST_PUBLIC_KEY = 'REQUEST_PUBLIC_KEY'
    RESPONSE_PUBLIC_KEY = 'RESPONSE_PUBLIC_KEY'


sequence_number = 0


class Message:
    type: MessageType
    body: str
    sequence_number: int

    def __init__(self, type_e, body):
        global sequence_number
        self.public_key = ClientData.key.load_my_key()[0]
        self.type = type_e
        self.sequence_number = sequence_number
        sequence_number += 1
        self.body = body


class ReceivedMessage(Message):

    def __init__(self, from_username, from_chat, type_e, body):
        super().__init__(type_e, body)
        self.from_chat = from_chat
        self.from_username = from_username


class Request:
    path: str
    message: Message

    def __init__(self, path: str, message: Message):
        self.path = path
        self.message = message


client_username = None
rsa: RSAUtil = None


def setup_client(username):
    global client_username
    global rsa
    client_username = username
    rsa = RSAUtil(client_username)
    if username not in rsa.key_manager.public_keys:
        rsa.key_manager.generate_key()
    if "server" not in rsa.key_manager.public_keys:
        rsa.key_manager.store_public_key("server",
                                         ClassPersist.load(KeyManagement('server'), 'server_key').load_my_key()[0])


def call_server(path: str, body=None):
    if body is None:
        body = '{}'
    message = json.dumps({'path': path, "username": client_username, 'path_body_sign': '', 'body': body})
    enc = rsa.encrypt("server", message)
    result = requests.post('http://localhost:8022/', json={'encrypted_body': enc})
    if result.status_code // 100 != 2:
        print("ERROR:", result.content)
        exit(-1)
    if str(result.content) == "b'null'":
        return None

    return json.loads(rsa.decrypt(str(result.content)[3:-2]))


class MessageHandler:
    incoming_messages: List[ReceivedMessage] = []

    @staticmethod
    def login(username, password):
        global client_username, rsa
        client_username = username
        message = json.dumps(
            {"username": client_username, 'password': password, 'public_key': rsa.key_manager.get_my_public_key_str()})
        enc = rsa.encrypt("server", message)
        result = requests.post('http://localhost:8022/loginOrRegister', json={'encrypted_body': enc})
        if result.status_code // 100 != 2:
            print("ERROR:", result.content)
            exit(-1)
        return json.loads(rsa.decrypt(str(result.content)[3:-2]))

    @staticmethod
    def send_message(request: Request):
        # TODO: Do handshake if session doesn't have key
        # if ClientData.get_chat_secret(json.loads(request.message.body)['to_username']) is None:
        #    MessageHandler.get_key(json.loads(request.message.body)['to_username'])
        call_server(request.path, json.dumps({'type': request.message.type.name, 'body': request.message.body}))

    @staticmethod
    def get_key(chat_id: str):
        MessageHandler.send_message(
            Request('/user/get_public_key', Message(MessageType.REQUEST_PUBLIC_KEY,
                                                    json.dumps({
                                                        'to_user_name': chat_id,
                                                        'public_key': rsa.key_manager.get_my_public_key_str()
                                                    }))))

        MessageHandler.wait_for_message_from_chat(chat_id, MessageType.RESPONSE_PUBLIC_KEY)

    @staticmethod
    def wait_for_message_from_user(username, mtype: MessageType):
        while True:
            sleep(0.1)
            MessageHandler.update_messages()
            for m in MessageHandler.incoming_messages:
                if m.from_username == username and m.type == mtype:
                    MessageHandler.incoming_messages.remove(m)
                    return m

    @staticmethod
    def wait_for_message_from_chat(chat_id: str, mtype: MessageType):
        while True:
            MessageHandler.update_messages()
            for m in MessageHandler.incoming_messages:
                if m.from_chat == chat_id and m.type == mtype:
                    MessageHandler.incoming_messages.remove(m)
                    return m

    @staticmethod
    def get_new_normal_messages_from_user(username) -> List[ReceivedMessage]:
        MessageHandler.update_messages()
        messages = []
        for m in MessageHandler.incoming_messages:
            if m.from_username == username and m.from_chat is None and m.type == MessageType.NORMAL:
                MessageHandler.incoming_messages.remove(m)
                messages.append(m)
        return messages

    @staticmethod
    def get_new_normal_messages() -> List[ReceivedMessage]:
        MessageHandler.update_messages()
        messages = []
        for m in MessageHandler.incoming_messages:
            if m.type == MessageType.NORMAL:
                MessageHandler.incoming_messages.remove(m)
                messages.append(m)
        return messages

    @staticmethod
    def get_new_messages_from_user(username) -> List[ReceivedMessage]:
        MessageHandler.update_messages()
        messages = []
        for m in MessageHandler.incoming_messages:
            if m.from_username == username and m.from_chat is None:
                MessageHandler.incoming_messages.remove(m)
                messages.append(m)
        return messages

    @staticmethod
    def get_new_normal_messages_from_chat(chat_id: int):
        MessageHandler.update_messages()
        messages = []
        for m in MessageHandler.incoming_messages:
            if m.from_chat == chat_id and m.type == MessageType.NORMAL:
                MessageHandler.incoming_messages.remove(m)
                messages.append(m)
        return messages

    @staticmethod
    def update_messages():
        for m in call_server('/messages', '{"type": "NORMAL", "body": "{}"}'):
            MessageHandler.incoming_messages.append(ReceivedMessage(m[0], m[1], MessageType[m[2]], m[3]))
