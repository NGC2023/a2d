DAPNET paging messages are limited to 80 characters per message. To conserve
space, a2d messages follow the structure given below and will be delivered to
your pager:

SourceCall (DestinationSSID): Message

- **SourceCall:** The sender's callsign.
- **DestinationSSID:** Your callsign's SSID.
- **Message:** The message content.

**Example**: `NY3W-5(7): Hello OM!`

Here, `NY3W` is the sender's callsign, `7` is the SSID of the receiver's (your)
callsign (e.g., NY3W-7), and `Hello OM!` is the message. If the DestinationSSID
displays 0, it means the message is targeted for your callsign without any SSID.