a2d is designed with a web UI.

### Install a2d

You can install a2d from GitHub Packages. Download the Debian package from [a2d
GitHub Releases](https://github.com/NGC2023/a2d/releases). Navigate to the
directory where you downloaded the Debian package using the command line and run
the following command:

`sudo apt install -y ./<a2d package>.deb`

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

`sudo apt update`

`sudo apt install <package>`

### Uninstall a2d

To uninstall a2d, follow these steps. For a thorough removal of user
configuration files, it is advisable to uninstall the application after
performing a Factory Reset in the a2d portal (Check Resetting a2d portal
section). This ensures a clean removal of user-specific settings.

`sudo apt purge a2d`

However, please note that this command won't remove the core nginx server and
other dependencies that were installed alongside a2d. To completely remove all
a2d dependencies, you can use the following commands:

**Warning:** Removing dependencies may adversely impact other applications using
the dependencies. If you using nginx server for other applications or you using
it as a webserver, **DO NOT** remove nginx.

Removing nginx and its associated files:

`sudo apt -y remove --purge nginx nginx-common nginx-full nginx-core`

Remove nginx configuration files:

`sudo rm -rf /etc/nginx`

Remove nginx default configuration:

`sudo rm -rf /etc/default/nginx`

Remove nginx init.d script:

`sudo rm -rf /etc/init.d/nginx`

Remove nginx log files:

`sudo rm -rf /var/log/nginx`

Finally, perform an autoremove to clean up any remaining dependencies:

`sudo apt autoremove`

### Python 3 and Other Dependencies:

Ensure that Python 3 is available in your system to run a2d. All the required
dependencies will be automatically installed during the a2d installation
process. However, if you encounter any errors related to dependencies during the
a2d installation, please make sure the following packages are available on your
system in addition to Python 3:

1. python3-cryptography
2. python3-requests
3. python3-flask
4. python3-gunicorn
5. python3-psutil
6. python3-yaml
7. nginx (not default installation, suggested for remote access)
8. certbot (not default installation, suggested for remote access)

Gunicorn serves as the WSGI server that powers the a2d user interface, while
Nginx is used as a reverse proxy server. Certbot is essential for creating and
maintaining the required SSL certificates.

If you prefer to install dependencies manually, you can use the following
commands to install from the apt repository:

`sudo apt update`  
`sudo apt install <package>`

If you encounter any issues during installation, you can try running:

`sudo apt --fix-broken install`

This will help resolve any broken dependencies and ensure that a2d operates
smoothly on your system.