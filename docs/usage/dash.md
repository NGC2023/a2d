**Navigation Bar:** Provides convenient links and icons for easy access to
  various sections such as Server, Mode (Light, Dark, and Auto), Options, and
  Logout. The Options section includes Configuration, Advanced Options,
  Backup/Restore Configuration, Change PIN, and Information.

**Dashboard:** Displays Callsign, a2d Status, Run Interval, Last Run,
  Destination SSIDs. Start/Stop Relay buttons.

**System Health:** Displays CPU temperature, Memory usage, and CPU Load.

**APRS to DAPNET Transmits:** Shows logs of APRS to DAPNET transmitted messages.

a2d app offers three screen modes with Bootstrap v5.3 support: Light, Dark, and
Auto.

**Light Mode:** Provides a clean and bright interface for comfortable usage.

**Dark Mode:** Offers a sleek, darker interface that's easy on the eyes,
  especially in low-light conditions.

**Auto Mode:** Adapts to your local system settings, ensuring a seamless
  experience that aligns with your device's theme.

Choose the mode that suits your preferences and enhances your interaction with
the a2d app.

### Setup Configuration

If it's your first time, the dashboard will show 'Setup Configuration' instead
of your Callsign. Click "Configuration" listed in options in the navigation bar
to begin.

**To complete setup:**

1. Enter your HAM radio callsign in ALL CAPS without any SSID for Callsign (no
   ssid).
2. Input your APRS API Key from [aprs.fi](http://aprs.fi).
3. Provide your DAPNET account username and password.
4. Include your DAPNET transmitter group code. Each DAPNET transmitter belongs
   to a specific group. Find your code during transmitter configuration. You can
   find your transmitter group code when setting up your transmitter at
   [hampager.de](http://hampager.de).
5. Click "Set Config" to save.

***Note***: Your data is securely encrypted. In case of security concerns,
regenerate keys on respective websites and change passwords.

### Start/Stop Relay

**Important:** Setup Configuration before pressing 'Start Relay' button.

- After configuring, click "Start Relay" to begin and "Stop Relay" in the
  dashboard to halt.
- The interval between each APRS to DAPNET transfer is managed by the crontab
  manager in your system. For example, if the transfer interval is set to 15
  min, cron will trigger the transfer at 0, 15, 30, and 45 min past the hour.
- a2d is designed to transfer only APRS messages received after its first run,
  preventing flooding DAPNET with a large number of messages all at once.

### Advanced Options

**Note:** APRS servers block requests under 2 min. Please set intervals > 5 min
for optimal performance.

If needed, modify in "Advanced Options" via "Options" in the navigation bar and
selecting "Advanced."

- **Interval:** Set retrieval frequency. Default is 15 minutes. Avoid very short
  intervals (below 5 min).
- **Preferred APRS SSIDs:** Define target SSIDs for messages. -0 is your
  callsign without SSID. Find HAM APRS SSIDs on [APRS SSID
  list](http://www.aprs.org/aprs11/SSIDs.txt).
- **Transmit logs:** Set displayed logs on dashboard.

### Backup/Restore Configuration

Once you've set up your a2d configuration, you can use the Backup/Restore in the
navigation bar to safeguard your settings. Both actions—backup and
restore—require Passphrase verification.

**Backup:** Create a backup of your a2d configuration files. The backup file's
name will be "a2d_config_backup.bin." This file is encoded binary and holds your
API credentials. Store it securely.

**Restore:** If you want to revert to a previous configuration, use the backup
file to restore. However, be cautious. If the bin file has been tampered with,
the restore won't work, and using a modified bin file is strongly discouraged.

Note: Safeguard your settings with backups and restorations, but secure your bin
file from unauthorized access and exercise caution to maintain the integrity of
your a2d configuration.

#### Errors while Backup/Restore:

- **Invalid Passphrase:** Retry with the correct Passphrase.
- **Configuration files missing:** Set up Configuration.
- **Invalid file:** During restore configuration, use the correct
  a2d_config_backup.bin file.
- **Configuration file tampered:** If you spot this, avoid using the modified
  file as it could harm the a2d app.