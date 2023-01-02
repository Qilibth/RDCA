import json

with open("user_database.json", "r") as user_database_file:
    a = (json.load(user_database_file)["IDS"])
    a.append("asd")
