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
                elif command == MAKE_ONLINE:
                    self.make_user_online(value, conn)
                elif command == MAKE_OFFLINE:
                    self.make_user_offline(value)
                elif command == RDC:
                    eligible_for_rdp = self.check_user_rdp(value)
                    if eligible_for_rdp:
                        self.remote_desktop_connection()
                    elif not eligible_for_rdp:
                        self.send(f"{RDC}//False")

    def remote_desktop_connection(self, requester_connection_object, requestee_connection_object):


    def check_user_rdp(self, id):
        for user_id in self.client_connection_list:
            if id == user_id and self.client_connection_list[id]["isOnline"]:
                return True
        return False

    def make_user_offline(self, id):
        self.client_connection_list[id]["isOnline"] = False
        self.client_connection_list[id]["ConnectionObject"] = None

    def make_user_online(self, id, conn):
        self.client_connection_list[id]["isOnline"] = True
        self.client_connection_list[id]["ConnectionObject"] = conn

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