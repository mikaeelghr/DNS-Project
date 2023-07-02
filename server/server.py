import json
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from server.data import Data, RequestBody, MessageToGroupRequestBody, MessageToUserRequestBody, \
    RemoveFromGroupRequestBody, MessageToUserLoginRequestBody, LoginOrRegisterRequestBody, GetNewMessages
from utils.key_manager import KeyManagement
from utils.password_utils import check_password
from utils.rsa_utils import RSAUtil

rsa = RSAUtil('server')


class EncryptedMessageRequestBody(BaseModel):
    # hex string
    encrypted_body: str


def decrypt(enc: EncryptedMessageRequestBody) -> Dict[str, Any]:
    json_str = rsa.decrypt(enc.encrypted_body)
    return json.loads(json_str)


app = FastAPI()


@app.post("/loginOrRegister")
def login_or_register_user(enc: EncryptedMessageRequestBody):
    body = LoginOrRegisterRequestBody(**decrypt(enc))
    print(body)
    if body.username in rsa.key_manager.public_keys:
        if KeyManagement.public_key_to_str(rsa.key_manager.get_public_key(body.username)) != body.public_key:
            raise HTTPException(status_code=401, detail="public keys must be equal")
        if not check_password(body.password, Data.users.get(body.username)[1]):
            raise HTTPException(status_code=401, detail="password is wrong")
        return rsa.encrypt(body.username, json.dumps({'result': 'login successfully'}))
    else:
        Data.save_user(body.username, body.password, body.public_key)
        rsa.key_manager.store_public_key(body.username, KeyManagement.str_to_public_key(body.public_key))
        return rsa.encrypt(body.username, json.dumps({'result': 'successful registration'}))


@app.post("/")
def handle_request(enc: EncryptedMessageRequestBody):
    request = RequestBody(**decrypt(enc))

    username = request.username

    if username not in rsa.key_manager.public_keys:
        raise HTTPException(status_code=403, detail="you must login")

    body = request.get_body()

    if isinstance(body, MessageToGroupRequestBody):
        Data.send_message_to_group(username, body)
    elif isinstance(body, MessageToUserRequestBody):
        Data.send_message_to_user(username, body)
    elif isinstance(body, RemoveFromGroupRequestBody):
        Data.remove_user_from_group(username, body)
    elif isinstance(body, MessageToUserLoginRequestBody):
        Data.send_message_user_login(username, body)
    elif isinstance(body, GetNewMessages):
        result = Data.get_new_messages(username)
        return rsa.encrypt(username, json.dumps(result))
