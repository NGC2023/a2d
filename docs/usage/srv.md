a2d offers server settings and advanced options for users who want to customize
their server. Make changes cautiously. You can use a2d with its default settings
for local access. If you want to access a2d from outside your network, you can
do so by making careful adjustments to your router's firewall settings.

### Server Page Overview

- **Navigation Bar:** Convenient links and icons for easy navigation are
  available, allowing you to access sections like Dashboard, Mode (Light, Dark,
  and Auto), Options, and Logout. The Options section includes Server
  Configuration, Self-Signed SSL, CA Signed SSL, Change PIN, Reset Portal,
  Logout, and Information.

- **Server Status:** Provides essential information, including the start time of
  Nginx and Gunicorn, Listen Port, Server Name, SSL Status, and SSL Certificate
  details such as Common Name (CN), Organization Name (O), and Expiry Date.

- **Network Health:** Displays the Round Trip Time (RTT) to APRS and DAPNET
  servers, indicating the speed at which data can transfer between your system
  and their servers.

### Server Configuration (Only if nginx & certbot installed)

The server configuration allows you to modify a2d's default server settings.
a2d's default settings include Listen Port: 9331, Server Name: _, and SSL
disabled.

These settings have the potential to override your existing NGINX configuration,
particularly if NGINX is configured for another application. If you are using
NGINX for another application, it is strongly recommended to manually configure
NGINX for a2d.

#### Desired Listen Port:
You can choose the port number for a2d access. For standard HTTP, it's port 80,
and for HTTPS, it's 443. Alternatively, you can select any other open port on
your system. After changing the port, you'll need to access a2d using the
specified port.

#### Desired Server Name:
You can set the server name to match your desired domain name. Ensure that the
server name corresponds to your domain name, especially if you've enabled SSL,
as it should match the Common Name (CN) in the SSL certificate.

#### Choosing SSL Certificates:
a2d offers the option to create and use either Self-Signed SSL or Certificate
Authority (CA) SSL certificates for your convenience. The difference between
them is the appearance of a green lock symbol in the browser when you access
them. Ensure that your server name matches the CN in your certificate before
making a choice. Before selecting an SSL option, you need to create the
certificates.

#### Creating Self-Signed SSL Certificate:
In a2d, you can create and store one self-signed SSL certificate. There's no
limit to how many times you can create it. You can generate it through the "Self
Signed SSL" link in the navigation bar or by clicking the green "Self Signed
SSL" button inside Server Configuration. Self-Signed SSL certificates are not
verified, so you'll encounter an SSL security warning when accessing a2d in a
web browser. You'll need to bypass this warning to access a2d once Self-Signed
SSL is enabled. Once you enabled SSL certificate access a2d through HTTPS.

#### Creating CA SSL Certificate:
a2d offers the option to create CA SSL certificates directly through certbot and
Let's Encrypt within the a2d portal. You can create them via the "CA Signed SSL"
link in the navigation bar or by clicking the green "CA Signed SSL" button
inside Server Configuration. You can generate as many CA Signed SSL certificates
as needed. Ensure that the Common Name (CN) matches your domain name. Once
you've created your desired SSL certificate, you can return to Server
Configuration to set it for a2d. After certificate creation, a2d uses certbot
for auto-renewal. If you no longer need CA SSL certificates, a2d provides an
option to delete them by clicking "Delete CA SSL" in the CA Signed SSL and
selecting the certificate to remove.

Please note that Let's Encrypt has a limit on duplicate certificates. For more
details, refer to [Let's Encrypt's
documentation](https://letsencrypt.org/docs/duplicate-certificate-limit/).

#### Firewall Settings:
Understanding your firewall settings is crucial. Carefully open the necessary
ports on your router to achieve the following:
1. Access a2d from outside your network.
2. Generate CA SSL certificates. Let's Encrypt will use ports 80 and 443 to
   validate your server before issuing the certificate. If you have both IPv4
   and IPv6, it's strongly recommended to open required ports for both IPv4 and
   IPv6. After generating certificates you can safely close them and leave 443
   open if you want remove access to a2d outside of your network.

In case you are unable to open the ports for some reason and cannot generate
Let's Encrypt certificates using the a2d portal, you can perform these tasks via
the command line and adjust your DNS settings on your provider's website. For
certbot user guide, visit the [Certbot user
guide](https://eff-certbot.readthedocs.io/en/stable/using.html).

### Resetting a2d portal

a2d provides a Reset Portal option that allows you to reset the portal and
delete SSL certificates, if desired. You need to enter correct passphrase to
reset the portal. You can choose to retain the SSL certificates during the
factory reset. The Reset Portal option is available in the server page's
options. This action will delete all user files, configurations, and data. If
you are accessing a2d via SSL during the reset, the server settings will revert
to the default a2d settings, and you will need to access a2d through HTTP port
9331 after the reset.