# a2d - APRS to DAPNET portal

a2d is an application for transmitting APRS messages to DAPNET pagers, dedicated
to the HAM radio community usage.

## Description

a2d utilizes the APRS API to retrieve APRS messages for a callsign and relays
them to DAPNET for delivery to your pager device. It supports multiple SSIDs.

## Prerequisites and Installation

1. **Ham Radio License:** Ensure you hold a valid HAM radio license with a
   callsign. Transmitting signals complies with license regulations and local
   laws.

2. **APRS API Key:** Register on aprs.fi with your callsign to generate a
   confidential API Key for downloading APRS messages. Keep this key private.

3. **DAPNET User and Password:** Create a secure account on hampager.de for
   DAPNET. Additional steps may be required if you don't have an approved DAPNET
   pager or transmitter.

4. **Debian System with Internet Connection**: For optimal performance and
   convenience in HAM Radio applications, especially if you prefer a compact,
   standalone setup with internet access, we recommend using a Raspberry Pi. The
   Raspberry Pi offers a cost-effective solution that's well-suited for these
   purposes.

**Compatibility**
- **Debian 12**: a2d has been thoroughly tested on Debian 12.
- **Debian 12 (VMware)**: Tested on Debian 12 within a VMware environment.
- **Raspberry Pi OS with Debian 12 (bookworm)**: Tested on Raspberry Pi OS with
  Debian version 12 (bookworm).

You can utilize various packages like VNC or SSH to set up your Raspberry Pi
even if you intend to run it headlessly (without a physical display). This
approach provides flexibility while maintaining a small footprint, making it a
versatile choice for HAM Radio enthusiasts.

**Installation:**  
You can install a2d from GitHub Packages. Download the Debian package from [a2d
GitHub Releases](https://github.com/NGC2023/a2d/releases). Navigate to the
directory where you downloaded the Debian package using the command line and run
the following command:

`sudo apt install -y ./<a2d package>.deb`

`sudo apt install -y ./<a2d-doc package>.deb`

Replace a2d_package_version.deb with the a2d file name you downloaded before
running this command.

To enable access to a2d over the network from another system, it is suggested to
install additional packages like nginx and certbot.

While the a2d interface supports any reverse proxy and HTTP server, it provides
options for limited management of nginx. However, please note that nginx is not
installed by default. If you choose to use nginx, you will need to install and
can configure via a2d.

To create and maintain CA SSL certificates, certbot is required. certbot is not
installed by default but is essential for generating CA SSL certificates and
managing them automatically. The a2d interface works with certbot to handle SSLs
related to a2d.

Install nginx and certbot:

`sudo apt update` `sudo apt install <package>`

To **uninstall a2d**, follow these steps. For a thorough removal of user
configuration files, it is advisable to uninstall the application after
performing a Factory Reset in the a2d portal (Check Resetting a2d portal
section). This ensures a clean removal of user-specific settings.

`sudo apt purge a2d`

However, please note that this command won't remove the core nginx server and
other dependencies that were installed alongside a2d. 
    
## Configuration and Usage

a2d is designed with a web UI.

For detailed documentation on how to use and configure a2d, please visit our
[GitHub Pages](https://ngc2023.github.io/a2d/) or access the locally installed
documentation through the `a2d-doc` deb package.
