document.addEventListener('DOMContentLoaded', function() {
    async function updateServiceStatus() {
        try {
            const [serviceStatusResponse, dashResponse] = await Promise.all([
                fetch('/service-status'),
                fetch('/for-dash')
            ]);

            const serviceStatusData = await serviceStatusResponse.json();
            const dashData = await dashResponse.json();

            const serviceStatusDiv = document.getElementById('service-status');
            const lastRunDiv = document.getElementById('last-run');
            const runIntervalDiv = document.getElementById('run-interval');
            const ssidDisplayDiv = document.getElementById('ssids-display');
            const labelElement = document.getElementById('get-callsign2');
            const callsignDiv = document.getElementById('get-callsign');
            
            const statusMessage = serviceStatusData.service_status.status_message;
            const colorStatus = serviceStatusData.service_status.color_status;

            if (colorStatus) {
                serviceStatusDiv.innerHTML = '<strong>Status: </strong>' + statusMessage;
            } else {
                serviceStatusDiv.innerHTML = '<strong>Status: <span style="color: #d4660c;">' + statusMessage + '</span></strong>';
            }

            lastRunDiv.innerHTML = '<strong>Last Run: </strong>' + dashData.last_run_human;
            runIntervalDiv.innerHTML = '<strong>Run Interval: </strong>' + dashData.run_interval;
            ssidDisplayDiv.innerHTML = '<strong>Destination SSIDs: </strong>' + dashData.ssids_display;
            labelElement.textContent = dashData.callsign2;
            
            const callsign = dashData.callsign;
            if (callsign === 'Setup Configuration') {
                callsignDiv.innerHTML = '<strong>Call Sign: </strong><strong><span style="color: #d4660c;">' + callsign + '</span></strong>';
            } else {
                callsignDiv.innerHTML = '<strong>Call Sign: </strong>' + callsign;
            }
            
        } catch (error) {
            console.error('Error fetching and updating data:', error);
        }

        fetch('/system-info')
            .then(response => response.json())
            .then(data => {
                const cpuTemperatureElement = document.getElementById('cpu-temperature');
                const systemMemoryUsageElement = document.getElementById('system-memory-usage');
                const cpuLoadElement = document.getElementById('cpu-load');

                cpuTemperatureElement.innerHTML = '<strong>CPU Temp: </strong>' + data.cpu_temperature;
                systemMemoryUsageElement.innerHTML = '<strong>Memory Usage: </strong>' + data.system_memory_usage;
                cpuLoadElement.innerHTML = '<strong>CPU Load: </strong>' + data.cpu_load;
            })
            .catch(error => {
                console.error('Error fetching server data:', error);
            });
    }

    updateServiceStatus();

    setInterval(updateServiceStatus, 5000);
});
