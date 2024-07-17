# a2d Changelog

All notable changes to a2d will be documented in this file.

## [Version 2.0.4] - 2024-07-17

### Changed
- **[Change]**: Included tests for a2d.
- **[Change]**: Updated dependencies in pyproject.toml.
- **[Change]**: Set default port number in a2d.desktop
to 9333.

### Removed
- **[Removal]**: Removed nginx and certbot as hard
dependencies.

## [Version 2.0.3] - 2023-10-27

### Changed
- **[Change]**: Transition to a consolidated single Python
package approach.

## [Version 2.0.1] - 2023-10-09

### Added
- **[Feature]**: Message counts added to APRS to DAPNET
Transmit logs.

### Changed
- **[Change]**: Optimized multicore processing for
dual-core processors, like the Raspberry Pi Zero 2 W.

### Security
- **[Security fix]**: Implemented yaml safe_load instead
of pickle for a2d configuration backup.

## [Version 2.0.0] - 2023-09-01

### Added
- **[Feature]**: Introduced a user-friendly Flask web app 
to enhance the a2d experience.
  - The UI now displays a2d status and message logs.
  - Implemented both light and dark modes for a visually 
  appealing user interface.
  - Enhanced security with PIN access protected by a
  Passphrase for the UI.
  - Users can now back up and restore a2d configurations
  conveniently.
  - Added an Instructions section to guide users within
  the UI.
  - Implemented an automatic logout feature after 30 min of
  inactivity.
  - Introduced automated APRS fetch interval management to
  prevent APRS account lock.
  - Users can now access listen port, server name, and 
  manage SSL certificates (self-signed and CA).
  - Introduced an option to select a2d default settings.
  - Implemented a factory reset feature for a2d, users can
  retain SSL certificates.
  - Enhanced server status UI with all status including SSL
  and certificate in use.
  - Added network health monitoring to track round trip
  time (RTT) to APRS and DAPNET servers.
  - Included clear notifications and feedback messages in 
  the UI based on user interactions.

### Changed
- **[Change]**: Accelerated data processing by utilizing 
multiprocessing for efficient multicore utilization.
- **[Change]**: Consolidated multiple system services into
a single, resource-efficient system service.
- **[Change]**: Streamlined installation by transitioning
from the pip repository to the apt repository for
dependencies.
- **[Change]**: Improved session management with the
introduction of the auto logout feature.
- **[Change]**: Enhanced database read/write operations
and implemented self-healing mechanisms if data corruption
occurs.

### Deprecated
- **[Deprecation]**: Deprecated the use of terminal and 
SSH commands for setting up and running a2d.

### Removed
- **[Removal]**: Eliminated terminal access to user data,
replacing it with the new web app interface.
- **[Removal]**: Removed a2d_core services, adopting a more
efficient cron job-based approach to improved efficiency 
and resource usage.

### Fixed
- **[Bug fix]**: Addressed an issue where the database was
being unnecessarily written during each run.
- **[Bug fix]**: Resolved database corruption in specific
scenarios.
- **[Bug fix]**: Prevented message loss due to frequent
APRS fetch by introducing automated APRS fetch interval
management.

### Security
- **[Security fix]**: Implemented safeguards to prevent
flooding bulk messages to DAPNET during the initial run.
- **[Security fix]**: Optimized data transfer from ARPS
for improved efficiency.
- **[Security fix]**: Strengthened data transfer to
DAPNET with enhanced error handlingfor incorrect
credentials.

## [Version 1.0.0] - 2023-06-23

### Added
- **[Feature]**: Added a user-friendly input method for
gathering user information and configuring a2d.

### Changed
- **[Change]**: Enhanced security by implementing
encryption for user information.

### Fixed
- **[Bug fix]**: Resolved the issue where callsign 0 was
incorrectly representing the SSID.
