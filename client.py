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

    # TODO: Add sign up and sign in to message handler (last)
    # TODO: Add remove from group to message handler (last)
    # TODO: Add create group to message handler
    # TODO: Add add to group to message handler
    # TODO: Refresh key if session key is expired or new one is requested

    # TODO: Add seq. no to messages
    # TODO: Server should authenticate user before accepting messages (client should sign messages)

    # TODO: Add secret key for sessions
    # TODO: Use secret key to encrypt messages before sending to server

    # TODO: Encrypt private key with password

    to_username = input('send_message_to_username: ')
    message = input('message: ')
    MessageHandler.send_message(Request('/user/send', Message(MessageType.NORMAL, json.dumps({
        'to_username': to_username, 'message': message
    }))))
