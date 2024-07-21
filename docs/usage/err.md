Error messages play a crucial role in guiding you through issues. They appear in
two places:

### 1. Service Status Container in the Dashboard

If you encounter any of these errors, you'll see them next to "Status" in the
Service Status container. To resolve, ensure accurate information in your
configuration and restart the service.

- **Invalid APRS API key**
- **Incorrect APRS API key**
- **Incorrect DAPNET username or password**
- **Incorrect DAPNET callsign or txgroup**

DAPNET-related errors appear only when a new APRS message is received and a2d
attempts to transmit it to DAPNET.

### 2. Error Messages Triggered by Click on the Dashboard

For these errors, you'll see messages upon clicking. Solutions are provided
below:

- **Invalid PIN:** Retry with the correct PIN.
- **Invalid Passphrase:** Retry with the correct Passphrase.
- **Configuration files missing:** Set up Configuration.
- **Invalid file:** During restore configuration, use the correct
  a2d_config_backup.bin file.
- **Configuration file tampered:** If you spot this, avoid using the modified
  file as it could harm the a2d app.

### 3. Error Messages during Server Settings and SSL Certificates

- **Create Self-Signed SSL Certificate before Enabling:** Ensure that you have
  created the required SSL certificates before configuring the server for SSL.
- **Server and Common Name Mismatch:** Verify that your server name matches the
  Common Name (CN) of the certificate and corresponds to your domain name.
- **CA SSL Certificate Already Exists:** Try deleting the CA SSL certificate
  before attempting to create a duplicate certificate.
- **CA SSL Does Not Exist:** The SSL certificate you are trying to delete does
  not exist. Try refreshing the page.
- **Selected CA SSL or Server Name in Use:** Do not delete an SSL certificate
  while it is in use. First, change the SSL settings in the server, and then
  attempt to delete it.
- **Unknown Response from the Server:** This issue could be due to network
  problems, firewall blocking specific ports, or reaching Let's Encrypt's SSL
  certificate limits.
- **Failed to Update Server:** Your server may be offline or unreachable.

### Other Unknown Errors and Troubleshooting:

If new messages aren't reaching your DAPNET pager:

**Potential Causes:** Too frequent APRS requests, or issues with APRS or DAPNET
servers.

**Resolution:** Confirm server functionality and your Configuration setup. If
the problem persists, wait for a couple of runs, as a2d self-heals the database.
If the issue continues, reinstall a2d to fix message database corruption.
Database corruption may occur during message read/write interruptions, such as
power outages, memory loss, or system failures.