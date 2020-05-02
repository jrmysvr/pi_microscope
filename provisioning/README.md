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

# Setup streaming with gstreamer

On the Pi:

```bash
DEST_IP=10.42.0.1 # IP of PC when connected to Pi via USB OTG

gst-launch-1.0 -v rpicamsrc num-buffers=-1 ! video/x-raw,width=640,height=480, framerate=41/1 ! timeoverlay time-mode="buffer-time" ! jpegenc !  rtpjpegpay !  udpsink host=DEST_IP port=5001
```
_start_pi_stream_

On the PC
```bash
gst-launch-1.0 udpsrc port=5001 ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink
```
_consume_pi_stream__

---

## References:
https://hackaday.io/project/167996-pi-microscope
https://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/
https://www.raspberrypi.org/forums/viewtopic.php?t=213397

---
## Troubleshooting:

_On Ubuntu 18.04, I needed to modify the USB/Ethernet connection as described here: https://raspberrypi.stackexchange.com/questions/73523/connect-pi-zero-via-usb-rndis-gadget-to-ubuntu-17-04_
https://askubuntu.com/questions/1039907/how-to-share-wired-network-connection-in-18-04
    - Open nmtui
    - Edit connection (Wired connection 1)
    - Set IPv4 to "Link Local Only"
        - To share internet, select "Shared to other computers"
