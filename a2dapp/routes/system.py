import psutil
from flask import Blueprint, jsonify
from a2dapp.routes.auth import login_required

system_routes = Blueprint('system', __name__)

@system_routes.route('/system-info', methods=['GET'])
@login_required
def system_info():
    style = 'style="color: #d4660c; font-weight: bold;"'

    #CPU temperature
    raw_cpu_temperature = get_cpu_temperature()
    if raw_cpu_temperature is not None:
        cpu_temperature_value = float(raw_cpu_temperature)
        formatted_cpu_temperature = f" {cpu_temperature_value:.2f}°C"

        if cpu_temperature_value > 80:
            temperature_style = style
        else:
            temperature_style = ''
        
        cpu_temperature = f'<span {temperature_style}>{formatted_cpu_temperature}</span>'
    else:
        cpu_temperature = "Not available"

    #System memory
    raw_memory_usage = get_system_memory_usage()
    if raw_memory_usage is not None:
        memory_usage_value = float(raw_memory_usage)
        memory_usage = f" {memory_usage_value}%"
    
        if memory_usage_value > 80:
            memory_style = style
        else:
            memory_style = ''
        
        system_memory_usage = f'<span {memory_style}>{memory_usage}</span>'
    else:
        system_memory_usage = "Not available"
    
    #CPU load
    cpu_load = get_cpu_load()
    cpu_load = f" {cpu_load}%"

    system_data = {
            "cpu_temperature": cpu_temperature,
            "system_memory_usage": system_memory_usage,
            "cpu_load": cpu_load
        }

    return jsonify(system_data)

def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            temp_str = temp_file.read().strip()
            temp_milli_celsius = int(temp_str)
            temp_celsius = temp_milli_celsius / 1000.0
            return temp_celsius
    except Exception as e:
        print("An error occurred:", e)
    
    return None

def get_system_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_cpu_load():
    load = psutil.cpu_percent(interval=1)
    return load
