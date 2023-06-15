#!/bin/sh

sudo systemctl stop a2d_core.timer
sudo systemctl disable a2d_core.timer

sudo systemctl stop a2d_core.service
sudo systemctl disable a2d_core.service

echo "a2d services stopped."
