import os
import sys
import subprocess
from utils.config_valid import compare_values
from utils.decr_usrinfo import retrieve_usrinfo
from cryptography.fernet import Fernet

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'utils' directory to the Python module search path if not already present
utils_dir = os.path.join(current_dir, 'utils')
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

def main():
    # Retrieve user information using the retrieve_usrinfo() function
    data = retrieve_usrinfo()

    # Access the decrypted data
    callsign_nossid = data['callsign_nossid']
    txgroup = data['txgroup']
    DAPNET_USER = data['DAPNET_USER']
    DAPNET_PASS = data['DAPNET_PASS']
    APRSAPI_KEY = data['APRSAPI_KEY']

    # Build the config_data and default_config dictionaries
    default_config = {
        "callsign_nossid": "YOUR_CALLSIGN_WITHOUT_SSID_ALL_CAPS",
        "txgroup": "YOUR_DAPNET_TRANSMITTER_GROUP",
        "DAPNET_USER": "YOUR_DAPNET_USERNAME",
        "DAPNET_PASS": "YOUR_DAPNET_PASSWORD",
        "APRSAPI_KEY": "YOUR_APRS_API_KEY"
    }

    config_data = {
        "callsign_nossid": callsign_nossid,
        "txgroup": txgroup,
        "DAPNET_USER": DAPNET_USER,
        "DAPNET_PASS": DAPNET_PASS,
        "APRSAPI_KEY": APRSAPI_KEY
    }

    # Check the configuration values using the compare_values() function
    config_valid = compare_values(config_data, default_config)

    if not config_valid:
        print("Stopping a2d services.")
        print("Please input right keys in config - run a2d_user_input.sh to input keys.")
        
        # Stop a2d services
        script_path = "/usr/bin/stop_a2d.sh"
        subprocess.run(["bash", script_path], check=True)

    else:
        # Run the scripts one by one
        scripts = ["build_usrdbs.py", "push_a2d.py"]
        for script in scripts:
            script_path = "/usr/bin/a2d/" + script
            subprocess.call(["python", script_path])

if __name__ == "__main__":
    main()
