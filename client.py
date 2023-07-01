import threading
import socket

from MessageHandler import MessageHandler


class Connection(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def run(self):
        self.running = True
        self.connect()

        while self.running:
            try:
                data = self.socket.recv(1024)
                if data:
                    self.handle_data(data)
                else:
                    self.close()
            except socket.error as e:
                print("Socket error:", e)
                self.close()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            print("Connection error:", e)
            self.close()

    def send(self, data):
        try:
            self.socket.sendall(data)
        except socket.error as e:
            print("Socket error:", e)
            self.close()

    def handle_data(self, data):
        print("ss seid: ", data)
        MessageHandler.add(data)

    def close(self):
        self.running = False
        if self.socket:
            self.socket.close()


def main():
    host = '127.0.0.1'
    port = 12345

    connection = Connection(host, port)
    connection.start()

    while True:
        message = input("Enter a message to send: ")
        if message == 'exit':
            connection.close()
            break
        connection.send(message.encode())


if __name__ == "__main__":
    main()


