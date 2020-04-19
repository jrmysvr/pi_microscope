# Provisioning the Raspberry Pi Microscope

## Enable SSH
- Create a file called `ssh` inside of the boot partition in the raspberry pi SD

## Configure Wifi
- Copy `wpa_supplicant.conf` to `/etc/wpa_supplicant` of the main partition of the raspberry pi SD

## Enable Ethernet over USB
- Modify `config.txt` in the /boot partition of the raspberry pi SD.
    - Add the following line
```
...
# Enable Ethernet over USB (OTG)
dtoverlay=dwc2
...
```
- Modify cmdline.txt in the /boot partition of the raspberry pi SD.
    - Insert the following immediately after `rootwait`
```
modules-load=dwc2,g_ether
```

_`cmdline.txt`_
> ... rootwait modules-load=dwc2,g_ether ...

---

## References:
https://hackaday.io/project/167996-pi-microscope
https://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/

---
## Troubleshooting:

_On Ubuntu 18.04, I needed to modify the USB/Ethernet connection as described here: https://raspberrypi.stackexchange.com/questions/73523/connect-pi-zero-via-usb-rndis-gadget-to-ubuntu-17-04_
https://askubuntu.com/questions/1039907/how-to-share-wired-network-connection-in-18-04
    - Open nmtui
    - Edit connection (Wired connection 1)
    - Set IPv4 to "Link Local Only"
        - To share internet, select "Shared to other computers"
