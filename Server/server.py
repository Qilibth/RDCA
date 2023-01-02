import socket
import threading

from servernetworkprotocol import *

# this class mainly contains network related things
class Main:
    def __init__(self):
        self.client_connection_list = {}

        with open("user_database.json", "r") as user_database_file:
            user_ids = json.load(user_database_file)["IDS"]
            for user_id in user_ids:
                self.client_connection_list[user_id] = {"isOnline" : False, "ConnectionObject" : None}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        self.server.listen()
        while True:
            conn, addr = self.server.accept()

            thread = threading.Thread(target=self.handle_client, args=(conn, addr,))
            thread.start()

    def send(self, msg, conn):
        msg_length = len(msg)
        send_msg_length = str(msg_length).encode(FORMAT)
        send_msg_length += b" " * (HEADER - msg_length)

        conn.send(send_msg_length)
        conn.send(msg.encode(FORMAT))

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


                # command checking
                if command == DISCONNECT:
                    print("User Left")
                    break
                elif command == SIGNUP:
                    self.send(f"{SIGNUP_RESULT}//{self.sign_up(value, conn)}", conn)

    def sign_up(self, id, conn):
        if id in self.client_connection_list:
            return False
        else:
            self.client_connection_list[id] = {"isOnline":False, "ConnectionObject":None}
            with open("user_database.json", "r") as user_database_file:
                a = (json.load(user_database_file)["IDS"])

            with open("user_database.json", "w") as user_database_file:
                a.append(id)
                json.dump({"IDS":a}, user_database_file)
            return True

Main()