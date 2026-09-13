#!/usr/bin/env python3

import platform
import sys

if platform.system() != "Linux":
    print("linux_daemon.py can only run on Linux.")
    sys.exit(1)

"""
Linux-only background task daemon.

Run manually:
    python3 -m pip install -r requirements.txt
    python3 linux_daemon.py

Using a virtual environment:
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python linux_daemon.py


Trigger a task from terminal:

    # Refresh if the IP address changes
    echo -n refresh | nc -U /run/user/$(id -u)/lgtvvolumecontrol.sock

    # Volume Up
    echo -n volumeup | nc -U /run/user/$(id -u)/lgtvvolumecontrol.sock

    # Volume Down
    echo -n volumedown | nc -U /run/user/$(id -u)/lgtvvolumecontrol.sock

    # Toggle Mute On/Off
    echo -n mutetoggle | nc -U /run/user/$(id -u)/lgtvvolumecontrol.sock


Trigger a task from Ubuntu keyboard shortcut:

    # Refresh if the IP address changes
    /bin/sh -c 'printf "%s" refresh | /usr/bin/nc -U /run/user/1000/lgtvvolumecontrol.sock >/dev/null 2>&1'

    # Volume Up
    /bin/sh -c 'printf "%s" volumeup | /usr/bin/nc -U /run/user/1000/lgtvvolumecontrol.sock >/dev/null 2>&1'

    # Volume Down
    /bin/sh -c 'printf "%s" volumedown | /usr/bin/nc -U /run/user/1000/lgtvvolumecontrol.sock >/dev/null 2>&1'

    # Toggle Mute On/Off
    /bin/sh -c 'printf "%s" mutetoggle | /usr/bin/nc -U /run/user/1000/lgtvvolumecontrol.sock >/dev/null 2>&1'


Systemd (user service):
    1. Create:
       ~/.config/systemd/user/lgtvvolumecontrol.service

    2. Add:

       [Unit]
       Description=LGTV Volume Control Linux Daemon
       After=default.target

       # Replace `{full_path}/lgtv-volume-control` with the absolute project path.

       [Service]
       Type=simple
       WorkingDirectory={full_path}/lgtv-volume-control

       # Without venv:
       ExecStart=/usr/bin/python3 {full_path}/lgtv-volume-control/linux_daemon.py

       # With venv, use this instead:
       # ExecStart={full_path}/lgtv-volume-control/.venv/bin/python {full_path}/lgtv-volume-control/linux_daemon.py

       Restart=on-failure
       RestartSec=1

       [Install]
       WantedBy=default.target

    3. Enable and start:
       systemctl --user daemon-reload
       systemctl --user enable --now lgtvvolumecontrol.service

    4. Check status:
       systemctl --user status lgtvvolumecontrol.service

    5. View logs:
       journalctl --user -u lgtvvolumecontrol.service -f

Socket:
    /run/user/<UID>/lgtvvolumecontrol.sock

Example:
    /run/user/1000/lgtvvolumecontrol.sock
"""

import os
import socket
import threading
from lgtv_volume import LGTVVolumeControl

SOCKET_PATH = os.environ.get(
    "LGTVVOLUME_SOCKET",
    f"/run/user/{os.getuid()}/lgtvvolumecontrol.sock",
)

def refreshAll():
    global device, is_muted
    device = LGTVVolumeControl()
    is_muted = device.getVolumeStats()["muted"]

def volume_up():
    global device
    device.volumeUp()

def volume_down():
    global device
    device.volumeDown()

def mute_toggle():
    global device, is_muted
    if is_muted is not None:
        is_muted = not is_muted
        device.mute(is_muted)

refreshAll()
    
TASKS = {
    "refresh": refreshAll,
    "volumeup": volume_up,
    "volumedown": volume_down,
    "mutetoggle": mute_toggle
}

def main():
    os.makedirs(os.path.dirname(SOCKET_PATH), exist_ok=True)
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o600)
    server.listen(5)
    print(f"lgtvvolumecontrol listening on {SOCKET_PATH}")
    try:
        while True:
            connection, _ = server.accept()
            with connection:
                command = connection.recv(1024).decode().strip()
                task = TASKS.get(command)
                if task is not None:
                    threading.Thread(
                        target=task,
                        daemon=True,
                    ).start()
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)

if __name__ == "__main__":
    main()