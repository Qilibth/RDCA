import json
import os

import rdp
import signup

# checking weather the user has an id or not if so then calls functions accordingly
with open("client_data.json", "r") as client_data_file:
    has_id = json.load(client_data_file)["HasID"]
    if has_id:
        rdp.main()
    else:
        signup.main()

