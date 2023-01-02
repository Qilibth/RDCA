import json

with open("client_data.json", "r") as client_data_file:
    IP = json.load(client_data_file)["ServerIP"]
PORT = 5050
ADDR = (IP, PORT)
HEADER = 64
FORMAT = "utf-8"

DISCONNECT = "/x0"
SIGNUP = "/x1"
SIGNUP_RESULT = "/x2"