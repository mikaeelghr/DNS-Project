import os
import json
from utils.AESCipher import AESCipher
from utils.password_utils import get_hashed_password, check_password


class ManageFiles:
    @staticmethod
    def load_json_data(filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_json_data(data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def make_files():
        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump({}, f)

        if not os.path.exists("pubkeys.json"):
            with open("pubkeys.json", "w") as f:
                json.dump({}, f)

        if not os.path.exists("messages.json"):
            with open("messages.json", "w") as f:
                json.dump([], f)

    def add_user(self, username, password, serialized_pubkey):
        users = self.load_json_data("users.json")
        if username in users:
            return False

        users[username] = {
            "password": get_hashed_password(password),
        }
        keys = self.load_json_data("pubkeys.json")
        keys[username] = {
            "pubkey": serialized_pubkey,
        }

        self.save_json_data(users, "users.json")
        self.save_json_data(keys, "pubkeys.json")
        return True

    def add_message(self, message, username, key, timestamp):
        messages = self.load_json_data("messages.json")
        aes_cipher = AESCipher(key)
        encrypted_message = aes_cipher.encrypt(message)
        new_message = {
            "message": encrypted_message,
            "sender_username": username,
            "message_timestamp": timestamp
        }
        messages.append(new_message)
        self.save_json_data(messages, "messages.json")

    def user_login(self, username, password):
        users = self.load_json_data("users.json")
        if username in users:
            stored_password = users[username]["password"]
            return check_password(password, stored_password)
        return False
