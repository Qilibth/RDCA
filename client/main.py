import json
import os

from rdp import RDP_Main
import signup

# checking weather the user has an id or not if so then calls functions accordingly
with open("client_data.json", "r") as client_data_file:
    has_id = json.load(client_data_file)["HasID"]
    if has_id:
        main = RDP_Main()
        main.main()
    else:
        signup.main()

