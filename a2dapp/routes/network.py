import subprocess
import re
from flask import Blueprint, jsonify
from a2dapp.routes.auth import login_required

network_routes = Blueprint('network', __name__)

@network_routes.route('/get-rtt', methods=['GET'])
@login_required
def get_rtt():
    hosts = {"aprs": "api.aprs.fi", "dapnet": "www.hampager.de"}
    rtt_results = {}

    for key, host in hosts.items():
        try:
            result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True, timeout=5)
            output_lines = result.stdout.splitlines()

            rtt_line = [line for line in output_lines if "time=" in line]

            if rtt_line:
                rtt_match = re.search(r"time=(\d+(\.\d+)?)", rtt_line[0])
                if rtt_match:
                    rtt_value = float(rtt_match.group(1))
                    rtt_results[key + "_rtt"] = f"{rtt_value} ms"
                else:
                    rtt_results[key + "_rtt"] = "Unreachable"
            else:
                rtt_results[key + "_rtt"] = "Unreachable"

        except subprocess.TimeoutExpired:
            rtt_results[key + "_rtt"] = "Unreachable"

    return jsonify(rtt_results)
