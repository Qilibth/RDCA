import json

import RDP
import SignUp

with open("client_data.json", "r") as client_data_file:
    has_id = json.load(client_data_file)["HasID"]
    if has_id:
        rdp = RDP.RDP_GUI()
        rdp.run()
    else:
        sign_up = SignUp.SignUpGUI()
        sign_up.run()