# a2d - APRS to DAPNET portal

a2d is an application for transmitting APRS messages to DAPNET 
pagers, dedicated to the HAM radio community usage.

## Description

a2d utilizes the APRS API to retrieve APRS messages for a 
callsign and relays them to DAPNET for delivery to your 
pager device. It supports multiple SSIDs.

## Prerequisites and Installation

1. **Ham Radio License:** Ensure you hold a valid HAM radio
license with a callsign.Transmitting signals complies with
license regulations and local laws.

2. **APRS API Key:** Register on aprs.fi with your callsign
to generate a confidential API Key for downloading APRS 
messages. Keep this key private.

3. **DAPNET User and Password:** Create a secure account 
on hampager.de for DAPNET. Additional steps may be required 
if you don't have an approved DAPNET pager or transmitter.

4. **Debian System with Internet Connection**: For optimal 
performance and convenience in HAM Radio applications,
especially if you prefer a compact, standalone setup with
internet access, we recommend using a Raspberry Pi.
The Raspberry Pi offers a cost-effective solution that's
well-suited for these purposes.

**Compatibility**
**Debian 12**: a2d has been thoroughly tested on Debian 12.
**Debian 12 (VMware)**: Tested on Debian 12 within a 
VMware environment.
**Raspberry Pi OS with Debian 11 (bullseye)**: Tested on 
Raspberry Pi OS with Debian version 11 (bullseye).

    You can utilize various packages like VNC or SSH to 
    set up your Raspberry Pi even if you intend to run 
    it headlessly (without a physical display). This 
    approach provides flexibility while maintaining a 
    small footprint, making it a versatile choice for 
    HAM Radio enthusiasts.

    **Installation:**  
    You have two installation options for a2d. You can 
    either install it from the Apt repository or download 
    it from the GitHub Packages. Choose the installation
    method that best suits your needs. To install it from 
    the Apt repository run the following command in the 
    terminal:

    `sudo apt install a2d`

    Alternatively, you can install a2d from GitHub Packages.
    Download the Debian package from
    https://github.com/NGC2023/a2d. Navigate to the
    directory where you downloaded the Debian
    package using the command line and run the following
    command:  

    `sudo apt install -y ./a2d_package_version.deb`

    Replace a2d_package_version.deb with the a2d file name
    you downloaded before running this command.

    To **uninstall a2d**, follow these steps.

    `sudo apt remove --purge a2d`
    
    However, please note that this command won't remove the 
    core Nginx server and other dependencies that were 
    installed alongside a2d. To completely remove all a2d 
    dependencies, you can use the following commands:
    
    Remove Nginx and its associated files:

    `sudo apt -y remove --purge nginx 
    nginx-common nginx-full nginx-core`
    
    Remove Nginx configuration files:

    `sudo rm -rf /etc/nginx`
    
    Remove Nginx default configuration:

    `sudo rm -rf /etc/default/nginx`
    
    Remove Nginx init.d script:

    `sudo rm -rf /etc/init.d/nginx`
    
    Remove Nginx log files:

    `sudo rm -rf /var/log/nginx`
    
    Delete the Nginx user and group:

    `sudo deluser nginx`  
    `sudo delgroup nginx`
    
    Finally, perform an autoremove to clean up any remaining
    dependencies:

    `sudo apt autoremove`

5. **Python 3 and Other Dependencies**: Ensure that Python 3
is available in your system to run a2d. All the required
dependencies will be automatically installed during the a2d
installation process. However, if you encounter any errors
related to dependencies during the a2d installation, please
make sure the following packages are available on your system
in addition to Python 3:

    1. python3-cryptography
    2. python3-requests
    3. python3-flask
    4. python3-crontab
    5. python3-gunicorn
    6. nginx
    7. certbot
    8. python3-psutil

    Gunicorn serves as the WSGI server that powers the a2d 
    user interface, while Nginx is used as a reverse proxy
    server. Certbot is essential for creating and 
    maintaining the required SSL certificates.

    If you prefer to install dependencies manually, you 
    can use the following commands to install from the apt
    repository:

    `sudo apt update`  
    `sudo apt install <package>`  
    `sudo apt upgrade`
    
    If you encounter any issues during installation, you 
    can try running:

    `sudo apt --fix-broken install`

    This will help resolve any broken dependencies and 
    ensure that a2d operates smoothly on your system.

## Configuration and Usage

a2d version 2.0.0 is designed with a web UI.

## Accessing a2d UI

Once a2d is installed, open a web browser on a computer
connected to the local network and visit
http://localhost:9331 or http://ipaddress:9331. The default
a2d communication port is 9331 over http. Alternatively, you
can access the a2d portal directly from the application list
on your Linux GUI desktop after installing a2d.

## Register PIN and Passphrase

Security is paramount in the a2d portal. Here's how to 
safeguard your access:

**PIN Registration:** Choose a personalized six-digit PIN.
If this is your first time, select "Register" on the login
page to set your 6-digit PIN and Passphrase.

**Logging In:** After registration, use your assigned PIN 
to log in. The login session will automatically expire 
after 20 minutes of inactivity, ensuring the security of
your data.

**PIN Recovery:** If you forget your PIN, use your 
Passphrase to create a new one. Click "Forgot PIN!" on the
login page, verify with your Passphrase, and proceed to
set a new PIN.

Note: There's no Passphrase reset option. Reinstalling the
a2d app is the only recourse to reset your Passphrase.

## Dashboard Overview

- **Navigation Bar:** Provides convenient links and icons
for easy access to various sections such as Server, Mode
(Light, Dark, and Auto), Options, and Exit. The Options
section includes Configuration, Advanced Options,
Backup/Restore Configuration, Change PIN, and Information.
- **Dashboard:** Displays Callsign, a2d Status,
Run Interval, Last Run, Destination SSIDs. Start/Stop Relay
buttons.
- **System Health:** Displays CPU temperature, Memory usage,
and CPU Load.
- **APRS to DAPNET Transmits:** Shows logs of APRS to DAPNET
transmitted messages.

a2d app offers three screen modes with Bootstrap v5.3
support: Light, Dark, and Auto.

- **Light Mode:** Provides a clean and bright interface for
comfortable usage.
- **Dark Mode:** Offers a sleek, darker interface that's easy
on the eyes, especially in low-light conditions.
- **Auto Mode:** Adapts to your local system settings,
ensuring a seamless experience that aligns with your device's
theme.

Choose the mode that suits your preferences and enhances
your interaction with the a2d app.

## Setup Configuration

If it's your first time, the dashboard will show 'Setup
Configuration' instead of your Callsign. Click
"Configuration" listed in options in the navigation
bar to begin.

**To complete setup:**

1. Enter your HAM radio callsign in ALL CAPS without any SSID
for Callsign (no ssid).
2. Input your APRS API Key from [aprs.fi](http://aprs.fi).
3. Provide your DAPNET account username and password.
4. Include your DAPNET transmitter group code. Each DAPNET
transmitter belongs to a specific group. Find your code
during transmitter configuration. You can find your
transmitter group code when setting up your transmitter
at [hampager.de](http://hampager.de).
5. Click "Set Config" to save.

Note: Your data is securely encrypted. In case of security
concerns, regenerate keys on respective websites and
change passwords.

## Start/Stop Relay

**Important:** Setup Configuration before pressing 
'Start Relay' button.

- After configuring, click "Start Relay" to begin and
"Stop Relay" in the dashboard to halt.
- The interval between each APRS to DAPNET transfer
is managed by the crontab manager in your system. For
example, if the transfer interval is set to 15 min,
cron will trigger the transfer at 0, 15, 30, and 45 min
past the hour.
- a2d is designed to transfer only APRS messages received
after its first run, preventing flooding DAPNET with a
large number of messages all at once.

## Advanced Options

**Note:** APRS servers block requests under 2 min. Please
set intervals > 5 min for optimal performance.

If needed, modify in "Advanced Options" via "Options" in
the navigation bar and selecting "Advanced."

- **Interval:** Set retrieval frequency. Default is 15
minutes. Avoid very short intervals (below 5 min).
- **Preferred APRS SSIDs:** Define target SSIDs for 
messages. -0 is your callsign without SSID. Find HAM APRS 
SSIDs on
[APRS SSID list](http://www.aprs.org/aprs11/SSIDs.txt).
- **Transmit logs:** Set displayed logs on dashboard.

## Backup/Restore Configuration

Once you've set up your a2d configuration, you can
use the Backup/Restore in the navigation bar to safeguard
your settings. Both actions—backup and restore—require
Passphrase verification.

**Backup:** Create a backup of your a2d configuration
files. The backup file's name will be 
"a2d_config_backup.yaml." This file is encoded binary and
holds your API credentials. Store it securely.

**Restore:** If you want to revert to a previous 
configuration, use the backup file to restore. However,
be cautious. If the bin file has been tampered with, the
restore won't work, and using a modified bin file is
strongly discouraged.

Note: Safeguard your settings with backups and restorations,
but secure your bin file from unauthorized access and exercise
caution to maintain the integrity of your a2d configuration.

**Errors while Backup/Restore:**

- **Invalid Passphrase:** Retry with the correct Passphrase.
- **Configuration files missing:** Set up Configuration.
- **Invalid file:** During restore configuration, use the 
correct a2d_config_backup.yaml file.
- **Configuration file tampered:** If you spot this, avoid 
using the modified file as it could harm the a2d app.

## Message Structure

DAPNET paging messages are limited to 80 characters per 
message. To conserve space, a2d messages follow the structure
given below and will be delivered to your pager:

SourceCall (DestinationSSID): Message

- **SourceCall:** The sender's callsign.
- **DestinationSSID:** Your callsign's SSID.
- **Message:** The message content.

**Example**: `NY3W-5(7): Hello OM!`

Here, `NY3W` is the sender's callsign, `7` is the SSID of
the receiver's (your) callsign (e.g., NY3W-7), and `Hello OM!`
is the message. If the DestinationSSID displays 0, it means
the message is targeted for your callsign without any SSID.

## Server Settings
a2d offers server settings and advanced options for users who
want to customize their server. Make changes cautiously. You
can use a2d with its default settings for local access. If 
you want to access a2d from outside your network, you can 
do so by making careful adjustments to your router's
firewall settings.

## Server Page Overview

- **Navigation Bar:** Convenient links and icons for easy 
navigation are available, allowing you to access sections 
like Dashboard, Mode (Light, Dark, and Auto), Options, and 
Exit. The Options section includes Server Configuration,
Self-Signed SSL, CA Signed SSL, Change PIN, Reset Portal,
Exit, and Information.
- **Server Status:** Provides essential information,
including the start time of Nginx and Gunicorn, Listen 
Port, Server Name, SSL Status, and SSL Certificate details 
such as Common Name (CN), Organization Name (O), and 
Expiry Date.
- **Network Health:** Displays the Round Trip Time (RTT)
to APRS and DAPNET servers, indicating the speed at
which data can transfer between your system and their
servers.

## Server Configuration

The server configuration allows you to modify a2d's default 
server settings. a2d's default settings include Listen 
Port: 9331, Server Name: _, and SSL disabled.

These settings have the potential to override your existing
NGINX configuration, particularly if NGINX is configured 
for another application. If you are using NGINX for another
application, it is strongly recommended to manually configure 
NGINX for a2d.

**Desired Listen Port:** You can choose the port number for
a2d access. For standard HTTP, it's port 80, and for HTTPS,
it's 443. Alternatively, you can select any other open port
on your system. After changing the port, you'll need to
access a2d using the specified port.

**Desired Server Name:** You can set the server name to 
match your desired domain name. Ensure that the server name
corresponds to your domain name, especially if you've
enabled SSL, as it should match the Common Name (CN) in the
SSL certificate.

**Choosing SSL Certificates:** a2d offers the option to create
and use either Self-Signed SSL or Certificate Authority (CA)
SSL certificates for your convenience. The difference between
them is the appearance of a green lock symbol in the browser
when you access them. Ensure that your server name matches
the CN in your certificate before making a choice. Before
selecting an SSL option, you need to create the certificates.

**Creating Self-Signed SSL Certificate:** In a2d, you can
create and store one self-signed SSL certificate. There's no
limit to how many times you can create it. You can generate it
through the "Self Signed SSL" link in the navigation bar or by
clicking the green "Self Signed SSL" button inside Server
Configuration. Self-Signed SSL certificates are not verified,
so you'll encounter an SSL security warning when accessing a2d
in a web browser. You'll need to bypass this warning to access
a2d once Self-Signed SSL is enabled. Once you enabled SSL
certificate access a2d through HTTPS.

**Creating CA SSL Certificate:** a2d offers the option to
create CA SSL certificates directly through certbot and 
Let's Encrypt within the a2d portal. You can create them via
the "CA Signed SSL" link in the navigation bar or by clicking
the green "CA Signed SSL" button inside Server Configuration.
You can generate as many CA Signed SSL certificates as needed.
Ensure that the Common Name (CN) matches your domain name.
Once you've created your desired SSL certificate, you can
return to Server Configuration to set it for a2d. After
certificate creation, a2d uses certbot for auto-renewal. If
you no longer need CA SSL certificates, a2d provides an
option to delete them by clicking "Delete CA SSL" in the 
CA Signed SSL and selecting the certificate to remove.

Please note that Let's Encrypt has a limit on duplicate
certificates. For more details, refer to [Let's Encrypt's 
documentation](https://letsencrypt.org/docs/
duplicate-certificate-limit/).

**Firewall Settings:** Understanding your firewall settings is
crucial. Carefully open the necessary ports on your router to
achieve the following:
1. Access a2d from outside your network.
2. Generate CA SSL certificates. Let's Encrypt will use ports
80 and 443 to validate your server before issuing the
certificate. If you have both IPv4 and IPv6, it's strongly 
recommended to open required ports for both IPv4 and IPv6.
After generating certificates you can safely close them and
leave 443 open if you want remove access to a2d outside of
your network.

In case you are unable to open the ports for some reason and
cannot generate Let's Encrypt certificates using the a2d 
portal,you can perform these tasks via the command line and 
adjust your DNS settings on your provider's website. For
certbot user guide, visit the [Certbot user guide]
(https://eff-certbot.readthedocs.io/en/stable/using.html).

## Resetting a2d portal

a2d provides a Reset Portal option that allows you to reset
the portal and delete SSL certificates, if desired. You 
need to enter correct passphrase to reset the portal. You
can choose to retain the SSL certificates during the factory
reset. The Reset Portal option is available in the server
page's options. This action will delete all user files, 
configurations, and data. If you are accessing a2d via SSL
during the reset, the server settings will revert to the
default a2d settings, and you will need to access a2d 
through HTTP port 9331 after the reset.

## Error Messages

Error messages play a crucial role in guiding you through
issues. They appear in two places:

### 1. Service Status Container in the Dashboard

If you encounter any of these errors, you'll see them next
to "Status" in the Service Status container. To resolve,
ensure accurate information in your configuration and
restart the service.

- **Invalid APRS API key**
- **Incorrect APRS API key**
- **Incorrect DAPNET username or password**
- **Incorrect DAPNET callsign or txgroup**

DAPNET-related errors appear only when a new APRS message
is received and a2d attempts to transmit it to DAPNET.

### 2. Error Messages Triggered by Click on the Dashboard

For these errors, you'll see messages upon clicking.
Solutions are provided below:

- **Invalid PIN:** Retry with the correct PIN.
- **Invalid Passphrase:** Retry with the correct Passphrase.
- **Configuration files missing:** Set up Configuration.
- **Invalid file:** During restore configuration, use the 
correct a2d_config_backup.yaml file.
- **Configuration file tampered:** If you spot this, avoid
using the modified file as it could harm the a2d app.

### 3. Error Messages -Server Settings and SSL Certificates

- **Create Self-Signed SSL Certificate before Enabling:** 
Ensure that you have created the required SSL certificates
before configuring the server for SSL.
- **Server and Common Name Mismatch:** Verify that your
server name matches the Common Name (CN) of the certificate
and corresponds to your domain name.
- **CA SSL Certificate Already Exists:** Try deleting the CA
SSL certificate before attempting to create a duplicate 
certificate.
- **CA SSL Does Not Exist:** The SSL certificate you are
trying to delete does not exist. Try refreshing the page.
- **Selected CA SSL or Server Name in Use:** Do not delete
an SSL certificate while it is in use. 
First, change the SSL settings in the server, and then
attempt to delete it.
- **Unknown Response from the Server:** This issue could be
due to network problems, firewall blocking specific ports,
or reaching Let's Encrypt's SSL certificate limits.
- **Failed to Update Server:** Your server may be offline 
or unreachable.

**Other Unknown Errors and Troubleshooting:**

If new messages aren't reaching your DAPNET pager:

**Potential Causes:** Too frequent APRS requests, or issues
with APRS or DAPNET servers.

**Resolution:** Confirm server functionality and your 
Configuration setup. If the problem persists, wait for a
couple of runs, as a2d self-heals the database. If the
issue continues, reinstall a2d to fix message database
corruption. Database corruption may occur during message
read/write interruptions, such as power outages, memory 
loss, or system failures.
