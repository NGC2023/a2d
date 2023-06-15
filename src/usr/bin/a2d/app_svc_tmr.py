import configparser
import os

# Read the configuration file
config = configparser.ConfigParser()
config.read("/etc/a2d/adv_conf.ini")

# Retrieve the timer interval value
interval_minutes = int(config["Timer"]["IntervalMinutes"])

# Calculate the timer schedule based on the interval
schedule = f"{interval_minutes}min"

# Check if the timer value is already set in the .service file
service_path = "/lib/systemd/system/a2d_core.timer"
existing_schedule = None

with open(service_path, "r") as file:
    for line in file:
        if line.startswith("OnUnitActiveSec"):
            existing_schedule = line.strip().split("=")[1].strip()

# Compare existing schedule with the interval_minutes value
if existing_schedule == schedule:
    message = "Timer value is already set. No changes needed."
else:
    # Update the systemd timer configuration file
    with open(service_path, "w") as file:
        file.write(f"[Unit]\nDescription=APRS to DAPNET Service Timer\n\n")
        file.write(f"[Timer]\nOnUnitActiveSec={schedule}\n\n")
        file.write(f"[Install]\nWantedBy=timers.target\n")

    # Check if a2d_core.timer is running
    systemctl_status_cmd = "systemctl is-active --quiet a2d_core.timer"
    timer_running = (os.system(systemctl_status_cmd) == 0)

    if timer_running:
        # Reload the systemd configuration
        systemctl_cmd = "sudo systemctl daemon-reload"
        os.system(systemctl_cmd)
    else:
        message = "a2d_core.timer is not running. Systemd configuration reload skipped."
