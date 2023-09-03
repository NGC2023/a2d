// Variable to hold the interval ID
var logsInterval;

// Log updates
function updateLogs() {
    var logsContainer = document.getElementById("logs-container");

    // Make a fetch request to fetch new log entries
    fetch("/fetch-logs")
        .then(response => {
            if (!response.ok) {
                throw new Error("Request failed. Status: " + response.status);
            }
            return response.json();
        })
        .then(logs => {
            // Clear existing log entries
            logsContainer.innerHTML = "";

            if (logs.length > 0) {
                // Add new log entries
                logs.forEach(log => {
                    var logEntry = document.createElement("p");

                    // Split the log into parts: message_id, restOfLog
                    var parts = log.split(" > ");
                    var message_id = parts[0];
                    var restOfLog = parts.slice(1).join(" > ");

                    // Create a <span> element for the log entry
                    var logSpan = document.createElement("span");
                    logSpan.innerHTML = `<em>${message_id}</em>> ${restOfLog}`; // Apply italics to message_id

                    logEntry.appendChild(logSpan); // Append the <span> to the log entry
                    logsContainer.appendChild(logEntry);
                });
            } else {
                // Add 'No APRS messages' text
                var noMessagesElement = document.createElement("p");
                noMessagesElement.textContent = "No Transmits";
                logsContainer.appendChild(noMessagesElement);
            }
        })
        .catch(error => {
            // Request failed, handle error
            console.error("Failed to fetch log entries. Error:", error);
        });
}

// Periodically update logs every 3 seconds
logsInterval = setInterval(updateLogs, 3000);

// Stop fetching logs after 10 minutes (600,000 milliseconds)
setTimeout(function () {
    clearInterval(logsInterval);
}, 600000);
