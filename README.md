# LG TV Volume Control

<div align="center">

![Logo](icons/icon_original.png)

</div>

A simple desktop GUI application built with **CustomTkinter** and **pywebostv** to control the volume of an LG webOS TV.

This application is especially useful when an LG TV is being used as a **computer monitor**, allowing you to control the TV volume from your computer without needing to reach for the TV remote every time.

---

## Features
 - 🔊 Volume Up
 - 🔉 Volume Down
 - 🎚️ Set volume to a specific percentage
 - 🔇 Mute / Unmute toggle
 - 📺 Display current TV volume percentage
 - 🖥️ Simple CustomTkinter GUI
 - 🌐 Connect to an LG webOS TV over the local network

---

## Requirements
 - Python 3.x
 - LG TV running webOS
 - Computer and TV connected to the same local network
 - Other dependencies listed in `requirements.txt`

Install the required Python packages with:

```
pip install -r requirements.txt
```

---

## Installation
### 1. Clone the repository
```
git clone https://github.com/akarshit-1609/lgtv-volume-control.git
cd lgtv-volume-control
```

### 2. Create a virtual environment

Using a virtual environment is **optional but recommended**.

Create a virtual environment:
```
python -m venv venv
```

### 3. Activate the virtual environment
Windows
```
venv\Scripts\activate
```

macOS / Linux
```
source venv/bin/activate
```

After activation, install the dependencies:
```
pip install -r requirements.txt
```

### 4. Run the application
```
python main.py
```

---

## How to Use
### First-Time Connection

When you open the application for the first time, you need to connect it to your LG TV.

 - Make sure your **computer and LG TV are connected to the same network**.
 - Find the IP address of your LG TV.
 - Open the application.
 - Enter the TV's IP address in the **middle IP address input field**.
 - Click Enter.
 - Your TV may display a permission/authorization prompt.
 - Accept the permission on the TV to allow the application to connect.

Once connected, the application should display the current TV volume.

For example:
```
50%
```

If the volume display shows:
```
-%
```

it means the application is **not currently connected to the TV** or cannot retrieve the TV's volume information.

If the TV is successfully connected, the display should show a value such as:

```
25%
50%
75%
100%
```

### How to Find Your LG TV IP Address

The exact menu names can vary depending on your LG TV model and webOS version.

Generally, you can find the IP address from the TV's network settings:

 - Open **Settings** on your LG TV.
 - Go to **Network** or **Network Connection**.
 - Open the currently connected network.
 - Look for **IP Address**.
 - Copy the displayed IP address.

For example:
```
192.168.1.25
```

Enter this IP address into the application's IP address field.

#### Important

Your computer and TV must be connected to the **same local network**.

For example:
```
Computer → 192.168.1.10
TV       → 192.168.1.25
```


Both devices are on the same `192.168.1.x` network, so they can communicate with each other.

If the TV and computer are on different networks, the application may not be able to connect.

### Setting a Specific Volume

To set the TV volume to a specific percentage:

 - Enter a number in the **right-side volume input field**.
 - The value must be between **0 and 100**.
 - Click **Enter**.
 - The TV volume will be set to the specified percentage.

For example:
```
50
```

and then press **Enter** to set the TV volume to 50%.

Valid range:
```
0 - 100
```

### Volume Controls

The application provides the following controls:

| Control | Description |
| --- | --- |
| Volume Up | Increases the TV volume |
| Volume Down | Decreases the TV volume |
| Set Volume | Sets the volume to a value from 0–100 |
| Mute | Toggles mute/unmute |
| IP Address | Connects to the specified LG TV |

### First-Time TV Permission

When connecting to the TV for the first time, **LG webOS** may ask you to allow the computer/application to connect.

This permission is required for the application to communicate with the TV.

When the authorization prompt appears on the TV, **accept it**.

If you reject the request, the application will not be able to control the TV.

### Reconnecting to the TV

If the TV becomes disconnected, check the following:

 - The TV is powered on.
 - The computer and TV are connected to the same network.
 - The TV's IP address has not changed.
 - The TV allows network/device connections.
 - No firewall or network configuration is blocking the connection.

If the displayed volume changes back to:
```
-%
```

the application is likely no longer connected to the TV.

---

## Limitations

This application uses the `pywebostv` library to communicate with the LG webOS TV. Therefore, the application's compatibility and functionality are subject to the capabilities and limitations of that library and the LG webOS API.

## LG webOS Compatibility

The application is intended for LG TVs running **webOS**, but behavior may vary depending on:

 - TV model
 - webOS version
 - TV network configuration
 - Available webOS APIs
 - Changes made by LG to its software

Not every LG TV or webOS version is guaranteed to work.

## Network Requirement

The computer and TV generally need to be reachable on the **same local network**.

The application is not designed to control the TV through the internet from a different network.

## TV Must Be Reachable

The TV needs to be powered on and reachable over the network for the application to communicate with it.

If the TV is unavailable, the application cannot reliably retrieve or change the volume.

## Pairing / Authorization

The first connection may require authorization from the TV.

The application cannot bypass the TV's authorization mechanism.

## IP Address Can Change

Depending on your router's DHCP configuration, the TV's IP address may change.

If that happens, you may need to enter the new IP address into the application.

For a more permanent setup, you can consider assigning the TV a DHCP reservation/static lease through your router.

## Not a Full TV Remote

This application is intentionally designed for **volume control only**.

It does not attempt to provide all functions available on the original LG TV remote.

Currently available controls are:

 - Volume Up
 - Volume Down
 - Set Volume
 - Mute/Unmute

Features such as changing channels, launching applications, navigating menus, changing picture settings, and other remote-control functions are outside the scope of this project.

## Dependency on `pywebostv`

Communication with the TV depends on `pywebostv`.

If `pywebostv` does not support a particular TV model, webOS version, API operation, or connection scenario, this application may also be unable to support it.

For more information about the underlying library and its supported functionality, see the **[PyWebOSTV](https://github.com/supersaiyanmode/PyWebOSTV)** project documentation.

## Troubleshooting
### Volume shows `-%`

Check:

 - The TV is powered on.
 - The TV and computer are on the same network.
 - The IP address is correct.
 - The TV authorization request was accepted.
 - The TV is reachable from your computer.
 - Try entering the TV IP address again.

### The TV doesn't show the permission prompt

Make sure the IP address is correct and that the TV is reachable from your computer.

You can also restart the application and try connecting again.

### The application cannot connect

Verify that:
```
Computer → Same Network ← TV
```

For example:
```
Computer: 192.168.1.10
TV:       192.168.1.25
```

If the devices are connected to isolated networks, guest Wi-Fi, or networks with client isolation enabled, they may not be able to communicate.

---

## Disclaimer

This is an independent project and is not affiliated with or endorsed by LG Electronics.

LG, webOS, and related trademarks belong to their respective owners.

The application depends on the behavior and availability of the LG webOS APIs and the `pywebostv` library. Compatibility with every LG TV model and webOS version is not guaranteed.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
