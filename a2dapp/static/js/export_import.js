//Export
document.addEventListener("DOMContentLoaded", function () {
    const backupButton = document.getElementById("backupButton");
    const passphraseInput = document.getElementById("passphrase1");
    const errorMessage = document.getElementById("error-message");

    backupButton.addEventListener("click", async function () {
        // Get the passphrase from the input
        const passphrase = passphraseInput.value;

        // Create a new FormData object to send the passphrase
        const formData = new FormData();
        formData.append("passphrase", passphrase);
        formData.append("action", "export");

        try {
            // Use the Fetch API to make the POST request
            const response = await fetch("/export", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                // Create a download link for the binary file
                const blob = await response.blob();
                const link = document.createElement("a");
                link.href = window.URL.createObjectURL(blob);
                link.download = "a2d_config_backup.yaml";
                link.click();
                //Set timeout to redirect, works if autodownload enabled in browsers
                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            } else if (response.status === 400) {
                errorMessage.innerText = "Invalid Passphrase!";
            } else if (response.status === 401) {
                errorMessage.innerText = "Config files missing! Setup Config";
            } else {
                console.error("Backup failed");
                errorMessage.innerText = "Backup failed";
            }
        } catch (error) {
            console.error("Error during backup:", error);
            errorMessage.innerText = "Error during backup";
        }
    });
});


//Import
document.addEventListener("DOMContentLoaded", function () {
    const restoreButton = document.getElementById("restoreButton");
    const passphraseInput = document.getElementById("passphrase2");
    const importFileInput = document.getElementById("import_file");
    const errorMessage2 = document.getElementById("error-message2");

    restoreButton.addEventListener("click", async function () {
        // Get the passphrase and file from the inputs
        const passphrase = passphraseInput.value;
        const importFile = importFileInput.files[0];

        // Create a new FormData object to send the passphrase and file
        const formData = new FormData();
        formData.append("passphrase", passphrase);
        formData.append("import_file", importFile);
        formData.append("action", "import");

        try {
            // Use the Fetch API to make the POST request
            const response = await fetch("/import", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                // Import successful, redirect to the main page, server side redirect wont work
                window.location.href = "/";
            } else if (response.status === 400) {
                errorMessage2.innerText = "Invalid Passphrase!";
            } else if (response.status === 401) {
                errorMessage2.innerText = "Config file tampered! Don't use this file";
            } else if (response.status === 402) {
                errorMessage2.innerText = "Invalid a2d backup file!";
            } else {
                // Other error, log it
                console.error("Restore failed");
                errorMessage2.innerText = "Backup failed";
            }
        } catch (error) {
            console.error("Error during restore:", error);
            errorMessage2.innerText = "Error during backup";
        }
    });
});
