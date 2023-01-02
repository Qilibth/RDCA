import json


with open("client_data.json", "r") as client_data_file:
    data = json.load(client_data_file)
    data["HasID"] = True

with open("client_data.json", "w") as client_data_file:
    json.dump(data, client_data_file, indent=4)
    print(data)