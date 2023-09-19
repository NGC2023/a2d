// Button functions
document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.getElementById("loginButton");
    const registerButton = document.getElementById("registerButton");
    const digit1Input = document.getElementById("digit1Input");
    const digit2Input = document.getElementById("digit2Input");
    const digit3Input = document.getElementById("digit3Input");
    const digit4Input = document.getElementById("digit4Input");
    const digit5Input = document.getElementById("digit5Input");
    const digit6Input = document.getElementById("digit6Input");

    fetch("/check_pin_file")
    .then(response => response.text())
    .then(data => {
        if (data === "7965732062696e") {
            loginButton.disabled = false;
            registerButton.innerHTML = "Forgot PIN?";
            registerButton.value = "forgotpin";
            registerButton.addEventListener("click", function() {
                window.location.href = "/pin-change";
            });
            loginButton.addEventListener("click", function() {
                document.getElementById("pinForm").action = "/login";
                document.getElementById("pinForm").submit();
            });
            digit1Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
            digit2Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
            digit3Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
            digit4Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
            digit5Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
            digit6Input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    loginButton.click();
                }
            });
        } else {
            loginButton.disabled = true;
            registerButton.innerHTML = "Register";
            registerButton.value = "register";
            registerButton.addEventListener("click", function() {
                window.location.href = "/create-passphrase";
            });

            // Disable input fields
            digit1Input.disabled = true;
            digit2Input.disabled = true;
            digit3Input.disabled = true;
            digit4Input.disabled = true;
            digit5Input.disabled = true;
            digit6Input.disabled = true;
        }
    })
    .catch(error => {
        console.error("Error checking pin file:", error);
    });
});
