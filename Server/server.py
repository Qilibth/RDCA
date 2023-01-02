import socket
import threading

from servernetworkprotocol import *

class Socket:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        self.server.listen()
        while True:
            conn, addr = self.server.accept()

            thread = threading.Thread(target=self.handle_client, args=(conn, addr,))
            thread.start()

    def handle_client(self, conn, addr):
        while True:
            msg_length = conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                command, value = None, None

                try:
                    command, value = msg.split("//")
                except:
                    pass

                print(msg)
                # command checking
                if command == DISCONNECT:
                    print("User Left")
                    break


Socket()