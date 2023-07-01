class Data:
    groups_secrets: Dict[int, str] = dict()
    chats_secrets: Dict[str, str] = dict()

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