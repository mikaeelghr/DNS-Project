from typing import List


class MessageHandler:
    incoming_messages: List = None
    outgoing_messages: List = None

    @staticmethod
    def send_message(message):
        MessageHandler.outgoing_messages.append(message)

    @staticmethod
    def wait_for_message(prefix):
        while True:
            for m in MessageHandler.incoming_messages:
                if m.startwith(prefix):
                    MessageHandler.incoming_messages.remove(m)
                    return m

    # connection call it
    @staticmethod
    def add(message):
        MessageHandler.incoming_messages.append(message)

    # connection call it
    @staticmethod
    def get_messages():
        new_messages_to_sent = MessageHandler.outgoing_messages
        MessageHandler.outgoing_messages = []
        return new_messages_to_sent
