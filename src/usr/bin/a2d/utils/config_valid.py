import os

def compare_values(config_data, default_config):
    config_valid = True

    for key, value in default_config.items():
        if key in config_data and config_data[key] == value:
            print(f"Change value for {key} from the default value.")
            config_valid = False
        elif key not in config_data:
            print(f"{key} is not found in the .conf file.")
            config_valid = False

    if not config_valid:
        print("Please modify the keys in the '/etc/a2d/user_info.conf' file before running a2d.")

    return config_valid
