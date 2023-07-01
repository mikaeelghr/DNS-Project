import os
import json
import hashlib
import utils.AESCipher

hash = lambda text: hashlib.sha256(text.encode()).hexdigest()

class manageFiles:

    def load_json_data(self,filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return {}

    def save_json_data(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def make_files(self):
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
            "password": hash(password),
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
        encrypted_message = aes_cipher.encrypt(message, key)
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
            return hash(password) == stored_password
        return False
