import json
from typing import List
from enum import Enum

import requests

from utils.key_manager import KeyManagement
from utils.rsa_utils import RSAUtil
from utils.singleton_class import ClassPersist


class MessageType(Enum):
    # normal message
    NORMAL = 'NORMAL'
    SYSTEM_DIFFIE_HELLMAN_STEP1 = 'SYSTEM_DIFFIE_HELLMAN_STEP1'
    SYSTEM_DIFFIE_HELLMAN_STEP2 = 'SYSTEM_DIFFIE_HELLMAN_STEP2'


class Message:
    type: MessageType
    body: str

    def __init__(self, type_e, body):
        self.type = type_e
        self.body = body


class ReceivedMessage(Message):

    def __init__(self, from_username, from_chat, type_e, body):
        super().__init__(type_e, body)
        self.from_chat = from_chat
        self.from_username = from_username


class Request:
    path: str
    message: Message

    def __init__(self, path, message):
        self.path = path
        self.message = message


client_username = None
rsa = None


def setup_client(username):
    global client_username
    global rsa
    client_username = username
    rsa = RSAUtil(client_username)
    rsa.key_manager.store_public_key("server",
                                     ClassPersist.load(KeyManagement('server'), 'server_key').load_my_key()[0])


def call_server(path: str, body=None):
    if body is None:
        body = '{}'
    message = json.dumps({'path': path, "username": client_username, 'path_body_sign': '', 'body': body})
    enc = rsa.encrypt("server", message)
    return requests.post('http://localhost:8022/', json={'encrypted_body': enc}).json()


class MessageHandler:
    incoming_messages: List[ReceivedMessage] = []

    @staticmethod
    def send_message(request: Request):
        # TODO: Do handshake if session doesn't have key
        # TODO: Keep state of session in Data
        call_server(request.path, json.dumps({'type': request.message.type.name, 'body': request.message.body}))

    @staticmethod
    def wait_for_message_from_user(username, mtype: MessageType):
        while True:
            MessageHandler.update_messages()
            for m in MessageHandler.incoming_messages:
                if m.from_username == username and m.type == mtype:
                    MessageHandler.incoming_messages.remove(m)
                    return m

    @staticmethod
    def wait_for_message_from_chat(chat_id: int, mtype: MessageType):
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
