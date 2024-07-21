Once a2d is installed, open a web browser in the same computer and visit

`http://localhost:9333`

or

`http://ipaddress:9333`

The default a2d communication port is 9333 over http. If you installed nginx
then the port is ***9331*** (local and remote).

Alternatively, you can access the a2d portal directly from the application list
on your Linux GUI desktop after installing a2d.

### Register PIN and Passphrase

Security is paramount in the a2d portal. Here's how to safeguard your access:

**PIN Registration:** Choose a personalized six-digit PIN. If this is your first
time, select "Register" on the login page to set your 6-digit PIN and
Passphrase.

**Logging In:** After registration, use your assigned PIN to log in. The login
session will automatically expire after 20 minutes of inactivity, ensuring the
security of your data.

**PIN Recovery:** If you forget your PIN, use your Passphrase to create a new
one. Click "Forgot PIN!" on the login page, verify with your Passphrase, and
proceed to set a new PIN.

Note: There's no Passphrase reset option. Removing and Reinstalling the a2d
portal is the only recourse to reset your Passphrase (Warning: You will loose
all your a2d data). After uninstalling a2d, please use the following command to
remove any existing user configuration files before proceeding with the
reinstallation.

`sudo rm -r /etc/a2d`