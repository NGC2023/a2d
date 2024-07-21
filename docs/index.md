### a2d - APRS to DAPNET portal

a2d is an application for transmitting APRS messages to DAPNET pagers, dedicated
to the HAM radio community usage.

### Description

a2d utilizes the APRS API to retrieve APRS messages for a callsign and relays
them to DAPNET for delivery to your pager device. It supports multiple SSIDs.

### Prerequisites

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

### Compatibility

**Debian 12**: a2d has been thoroughly tested on Debian 12.

**Debian 12 (VMware)**: Tested on Debian 12 within a VMware environment.

**Raspberry Pi OS with Debian 12 (bookworm)**: Tested on Raspberry Pi OS with
  Debian version 12 (bookworm).

You can utilize various packages like VNC or SSH to set up your Raspberry Pi
even if you intend to run it headlessly (without a physical display). This
approach provides flexibility while maintaining a small footprint, making it a
versatile choice for HAM Radio enthusiasts.