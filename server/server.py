import json
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from server.data import RegisterRequestBody, Data, RequestBody, MessageToGroupRequestBody, MessageToUserRequestBody, \
    RemoveFromGroupRequestBody, GetNewMessages
from utils.rsa_utils import RSAUtil

rsa = RSAUtil('server')


class EncryptedMessageRequestBody(BaseModel):
    # hex string
    encrypted_body: str


def decrypt(enc: EncryptedMessageRequestBody) -> Dict[str, Any]:
    json_str = rsa.decrypt(enc.encrypted_body)
    return json.loads(json_str)


app = FastAPI()


@app.post("/register")
def register_user(enc: EncryptedMessageRequestBody):
    body = RegisterRequestBody(**decrypt(enc))
    Data.save_user(body.username, body.password, body.public_key)


@app.post("/")
def handle_request(enc: EncryptedMessageRequestBody):
    request = RequestBody(**decrypt(enc))

    username = request.username
    body = request.get_body()

    # TODO: Add access control (paniz)

    if isinstance(body, MessageToGroupRequestBody):
        Data.send_message_to_group(username, body)
    elif isinstance(body, MessageToUserRequestBody):
        Data.send_message_to_user(username, body)
    elif isinstance(body, RemoveFromGroupRequestBody):
        Data.remove_user_from_group(body)
    elif isinstance(body, GetNewMessages):
        result = Data.get_new_messages(username)
        # TODO: Encrypt result (paniz)
        # TODO: Add seq. no to messages (paniz)
        return result
