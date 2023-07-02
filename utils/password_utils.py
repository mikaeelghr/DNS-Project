import base64

import bcrypt


def get_hashed_password(password: str) -> str:
    return str(base64.b64encode(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())))[2:-1]


def check_password(password: str, hashed_password: str):
    x = base64.b64decode(hashed_password)
    return bcrypt.checkpw(password.encode('utf-8'), x)
