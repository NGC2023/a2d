#!/bin/bash

# Check if /usr/bin/a2d/a2d_usrk.bin already exists
if [ -e "/usr/bin/a2d/a2d_usrk.bin" ]; then
  # Change permissions and ownership
  sudo chmod 644 /usr/bin/a2d/a2d_usrk.bin
  sudo chown root:root /usr/bin/a2d/a2d_usrk.bin

  # Run create_usrinfo.py from /usr/bin/a2d directory
  cd /usr/bin/a2d
  sudo python create_usrinfo.py

  # Wait until create_usrinfo.py completes its task
  while pgrep -f "create_usrinfo.py" >/dev/null; do
    sleep 1
  done

  # Reset ownership and permissions
  sudo chown a2d:a2d /usr/bin/a2d/a2d_usrk.bin
  sudo chmod 400 /usr/bin/a2d/a2d_usrk.bin

else
  # Run create_usrinfo.py from /usr/bin/a2d directory
  cd /usr/bin/a2d
  sudo python create_usrinfo.py

  # Wait until create_usrinfo.py completes its task
  while pgrep -f "create_usrinfo.py" >/dev/null; do
    sleep 1
  done

  # Change ownership and permissions
  sudo chown a2d:a2d /usr/bin/a2d/a2d_usrk.bin
  sudo chmod 400 /usr/bin/a2d/a2d_usrk.bin
fi
