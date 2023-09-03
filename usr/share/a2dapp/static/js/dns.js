//HTML alert display box
document.addEventListener('DOMContentLoaded', function() {
    function updateServerData() {
        fetch('/for-html')
            .then(response => response.json())
            .then(data => {
                const listenPortElement = document.getElementById('listen-port');
                const serverNameElement = document.getElementById('server-name');
                const currentSSLStatusElement = document.getElementById('current-ssl-status');
                const commonNameElement = document.getElementById('common-name');
                const organizationNameElement = document.getElementById('organization-name');
                const expiryDateElement = document.getElementById('expiry-date');
                const nginxStatusElement = document.getElementById('nginx-status');
                const gunicornStatusElement = document.getElementById('gunicorn-status');

                listenPortElement.innerHTML = '<strong>Listen Port: </strong>' + data.listen_port;
                serverNameElement.innerHTML = '<strong>Server Name: </strong>' + data.server_name;
                currentSSLStatusElement.innerHTML = '<strong>SSL Status: </strong>' + data.current_ssl_status;
                commonNameElement.innerHTML = '<strong>Common Name (CN): </strong>' + data.common_name;
                organizationNameElement.innerHTML = '<strong>Organization Name (O): </strong>' + data.organization_name;
                nginxStatusElement.innerHTML = '<strong>Nginx:</strong> Active since ' + data.nginx_status;
                gunicornStatusElement.innerHTML = '<strong>Gunicorn WSGI:</strong> Active since ' + data.gunicorn_status;
                
                const expiryDate = data.expiry_date;
                if (expiryDate === 'Expired') {
                    expiryDateElement.innerHTML = '<strong>Expiry Date: </strong><strong><span style="color: #d4660c;">' + expiryDate + '</span></strong>';
                } else {
                    expiryDateElement.innerHTML = '<strong>Expiry Date: </strong>' + expiryDate;
                }
            
            })
            .catch(error => {
                console.error('Error fetching server data:', error);
            });
    }

    updateServerData();
    
    setInterval(updateServerData, 5000);
});


//Network health
document.addEventListener('DOMContentLoaded', function() {
    function updateNetworkData() {
        fetch('/get-rtt')
            .then(response => response.json())
            .then(data => {
                const aprsRttElement = document.getElementById('aprs-rtt');
                const dapnetRttElement = document.getElementById('dapnet-rtt');
                const aprsRtt = data.aprs_rtt;
                const dapnetRtt = data.dapnet_rtt;
                
                if (aprsRtt === 'Unreachable') {
                    aprsRttElement.innerHTML = '<strong>APRS RTT: </strong><strong><span style="color: #d4660c;">' + aprsRtt + '</span></strong>';
                } else {
                    aprsRttElement.innerHTML = '<strong>APRS RTT: </strong>' + aprsRtt;
                }

                if (dapnetRtt === 'Unreachable') {
                    dapnetRttElement.innerHTML = '<strong>DAPNET RTT: </strong><strong><span style="color: #d4660c;">' + dapnetRtt + '</span></strong>';
                } else {
                    dapnetRttElement.innerHTML = '<strong>DAPNET RTT: </strong>' + dapnetRtt;
                }
            })
            .catch(error => {
                console.error('Error fetching server data:', error);
            });
    }
    
    updateNetworkData();

    //first minute 10 sec, after that 120 sec
    var firstMinuteInterval = setInterval(updateNetworkData, 10000);

    setTimeout(function () {
        clearInterval(firstMinuteInterval);
        setInterval(updateNetworkData, 120000);
    }, 60000);
});


//Server Config
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("serverForm");
    const enableSSLCheckbox = document.getElementById("enable_ssl");
    const enableCASSLCheckbox = document.getElementById("enable_cassl");
    const setDefaultDnsCheckbox = document.getElementById("set_default_dns");    
    const serverMessage = document.getElementById("server-message");
    
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const listenPort = form.elements["listen_port"].value;
        const serverName = form.elements["server_name"].value;
        const caSSLCerts = form.elements["set_cassl_certs"].value;
        const enableSSL = enableSSLCheckbox.checked;
        const enableCASSL = enableCASSLCheckbox.checked;
        const setDefaultDns = setDefaultDnsCheckbox.checked;

        try {
            const formData = new FormData();
            formData.append("listen_port", listenPort);
            formData.append("server_name", serverName);
            formData.append("set_cassl_certs", caSSLCerts);
            formData.append("enable_ssl", enableSSL);
            formData.append("enable_cassl", enableCASSL);
            formData.append("set_default_dns", setDefaultDns);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            const result = await response.text();

            if (response.ok) {
                if (result === "Create SSL") {
                serverMessage.innerText = "Create self SSL certificate before enabling";
                } else if (result === "Create caSSL") {
                serverMessage.innerText = "Create/Select CA SSL certificate before enabling";
                } else if (result === "SN_CN no match") {
                serverMessage.innerText = "Server and Common Name mismatch";
                } else if (result === "caSSL enabled") {
                serverMessage.innerText = "CA SSL enabled";
                } else if (result === "Set default") {
                serverMessage.innerText = "Default to the original settings";
                } else if (result === "SSL enabled") {
                serverMessage.innerText = "Self-Signed SSL enabled";
                } else if (result === "Server updated") {
                serverMessage.innerText = "Server settings updated";
                } else {
                serverMessage.innerText = "Unknown response from the server";
                }
            } else {
                serverMessage.innerText = "Failed to update server";
            }
        } catch (error) {
        console.error("Error updating server", error);
        serverMessage.innerText = "Error updating server";
        }
    });
});


// JavaScript code to ensure only one checkbox is checked at a time
document.addEventListener("DOMContentLoaded", function() {
    const enableSSLCheckboxControl = document.getElementById('enable_ssl');
    const enableCASSLCheckboxControl = document.getElementById('enable_cassl');
    const setDefaultDNSCheckbox = document.getElementById('set_default_dns');
    const checkboxClickedInput = document.getElementById('checkbox_clicked');

    enableSSLCheckboxControl.addEventListener('click', function() {
        setDefaultDNSCheckbox.checked = false;
        enableCASSLCheckboxControl.checked = false;
        checkboxClickedInput.value = 'enable_ssl';
    });

    enableCASSLCheckboxControl.addEventListener('click', function() {
        setDefaultDNSCheckbox.checked = false;
        enableSSLCheckboxControl.checked = false;
        checkboxClickedInput.value = 'enable_cassl';
    });

    setDefaultDNSCheckbox.addEventListener('click', function() {
        enableSSLCheckboxControl.checked = false;
        enableCASSLCheckboxControl.checked = false;
        checkboxClickedInput.value = 'set_default_dns';
    });
});


//CA signed SSL
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("caSSLForm");
    const caSSLMessage = document.getElementById("cassl-message");

    form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const cacommonName = form.elements["ca_common_name"].value;
    const emailidName = form.elements["email_id"].value;

    try {  
        // Show "Generating..." message
        caSSLMessage.innerText = "Generating...";

        const formData = new FormData();
        formData.append("ca_common_name", cacommonName);
        formData.append("email_id", emailidName);

        const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        });

        const result = await response.text();

        if (response.ok) {
        if (result === "caSSL exist") {
            caSSLMessage.innerText = "CA SSL certificate already exists";
        } else if (result === "caSSL generated") {
            caSSLMessage.innerText = "CA SSL certificate generated";
        } else if (result === "invalid email") {
            caSSLMessage.innerText = "Enter valid email for certificate notifications";
        } else {
            caSSLMessage.innerText = "Unknown response from the server";
        }
        } else {
        caSSLMessage.innerText = "Failed to generate SSL certificate";
        }
    } catch (error) {
        console.error("Error generating SSL", error);
        caSSLMessage.innerText = "Error generating SSL certificate";
    }
    });
});


//Self signed SSL
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("selfSSLForm");
    const selfSSLMessage = document.getElementById("selfssl-message");

    form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const commonName = form.elements["common_name"].value;
    const validityDays = form.elements["validity_days"].value;
    const organizationName = form.elements["organization_name"].value;

    try {  
        // Show "Generating..." message
        selfSSLMessage.innerText = "Generating...";

        const formData = new FormData();
        formData.append("common_name", commonName);
        formData.append("validity_days", validityDays);
        formData.append("organization_name", organizationName);

        const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        });

        const result = await response.text();

        if (response.ok) {
        if (result === "sSSL generated") {
            selfSSLMessage.innerText = "SSL certificate generated";
        } else {
            selfSSLMessage.innerText = "Unknown response from the server";
        }
        } else {
        selfSSLMessage.innerText = "Failed to generate SSL certificate";
        }
    } catch (error) {
        console.error("Error generating SSL", error);
        selfSSLMessage.innerText = "Error generating SSL certificate";
    }
    });
});


//Remove CA SSL
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("rmcaSSLForm");
    const rmCaSSLMessage = document.getElementById("rmcassl-message");
    
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const rmcaSSLCerts = form.elements["rm_cassl_certs"].value;
        
        try {
            const formData = new FormData();
            formData.append("rm_cassl_certs", rmcaSSLCerts);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            const result = await response.text();

            if (response.ok) {
                if (result === "caSSL removed") {
                rmCaSSLMessage.innerText = "CA SSL Deleted";
                } else if (result === "Error removing SSL") {
                rmCaSSLMessage.innerText = "Error deleting CA SSL";
                } else if (result === "caSSL in use") {
                rmCaSSLMessage.innerText = "Selected CA SSL or Server Name in USE";
                } else if (result === "No caSSL") {
                rmCaSSLMessage.innerText = "CA SSL Do not Exist";
                } else {
                rmCaSSLMessage.innerText = "Unknown response from the server";
                }
            } else {
                rmCaSSLMessage.innerText = "Failed to delete CA SSL";
            }
        } catch (error) {
        console.error("Error deleting CA SSL", error);
        rmCaSSLMessage.innerText = "Error deleting CA SSL";
        }
    });
});


//Reset portal
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("resetForm");
    const passphraseInput = document.getElementById("passphrase");
    const selfSSLDELCheckbox = document.getElementById("self_ssl_delete");
    const caSSLDELCheckbox = document.getElementById("ca_ssl_delete");
    const resetMessage = document.getElementById("reset-message");
    
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const passphrase = passphraseInput.value;
        const resetConfirm = form.elements["reset_confirm"].value;
        const selfSSLDEL = selfSSLDELCheckbox.checked;
        const caSSLDEL = caSSLDELCheckbox.checked;

        try {
            // Show "Resetting..." message
            resetMessage.innerText = "Factory resetting...";

            const formData = new FormData();
            formData.append("passphrase", passphrase);
            formData.append("reset_confirm", resetConfirm);
            formData.append("self_ssl_delete", selfSSLDEL);
            formData.append("ca_ssl_delete", caSSLDEL);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            const result = await response.text();

            if (response.ok) {
                if (result === "Type delete") {
                resetMessage.innerText = "Type DELETE to confirm Factory Reset";
                } else if (result === "logout") {
                resetMessage.innerText = "Factory reset complete, you can safely logout";
                } else {
                resetMessage.innerText = "Unknown response from the server";
                }
            } else if (response.status === 400) {
                resetMessage.innerText = "Invalid Passphrase!";
            }
        } catch (error) {
        console.error("Error updating server", error);
        resetMessage.innerText = "Error Factory Resetting";
        }
    });
});
