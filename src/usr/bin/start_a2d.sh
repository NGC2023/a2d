#!/bin/sh

if ! systemctl is-active --quiet a2d_core.service; then
    sudo systemctl start a2d_core.service
    sudo systemctl enable a2d_core.service
fi

if ! systemctl is-active --quiet a2d_core.timer; then
    sudo systemctl start a2d_core.timer
    sudo systemctl enable a2d_core.timer
fi

echo "a2d services started."
