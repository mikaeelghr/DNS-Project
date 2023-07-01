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

"""
    for m in MessageHandler.get_new_messages_from_user(sys.argv[2]):
        if m.type == MessageType.NORMAL:
            if m.from_chat is not None:
                print('{} sent a message to chat#{}: {}'.format(m.from_username, m.from_chat, m.body))
            else:
                print('{} sent a message to you: {}'.format(m.from_username, m.body))
        elif m.type == MessageType.SYSTEM_DIFFIE_HELLMAN_STEP1:
            a = generate_b()
            MessageHandler.send_message(
                Request('/user/send', Message(MessageType.SYSTEM_DIFFIE_HELLMAN_STEP2, json.dumps({
                    'to_username': m.from_username, 'message': b
                }))))
    # ma -> ali : a
    # ali -> ma : b
    # -> secret

    MessageHandler.send_message(Request('/user/send', Message(MessageType.SYSTEM_DIFFIE_HELLMAN_STEP1, json.dumps({
        'to_username': 'reza', 'message': generate_a()
    }))))
    m = MessageHandler.wait_for_message_from_user(to_username, MessageType.SYSTEM_DIFFIE_HELLMAN_STEP2)
    b = m.body
    secret = a * b
"""
