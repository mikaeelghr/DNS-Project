import json

from MessageHandler import MessageHandler, setup_client, Request, Message, MessageType
import sys, select

username = sys.argv[1]

setup_client(username)

while True:
    for m in MessageHandler.get_new_normal_messages_from_user(sys.argv[2]):
        if m.from_chat is not None:
            print('{} sent a message to chat#{}: {}'.format(m.from_username, m.from_chat, m.body))
        else:
            print('{} sent a message to you: {}'.format(m.from_username, m.body))
    i, o, e = select.select([sys.stdin], [], [], 0.2)
    to_username = input('send_message_to_username: ')
    message = input('message: ')
    MessageHandler.send_message(Request('/user/send', Message(MessageType.NORMAL, json.dumps({
        'to_username': to_username, 'message': message
    }))))
