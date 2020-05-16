# Provisioning the Raspberry Pi Microscope

## Setup

### Enable SSH
- Create a file called `ssh` inside of the boot partition in the raspberry pi SD

### Configure Wifi
- Copy `wpa_supplicant.conf` to `/etc/wpa_supplicant` of the main partition of the raspberry pi SD

### Enable Ethernet over USB
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
modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:20 g_ether.dev_addr=00:22:82:ff:ff:22
```

_`cmdline.txt`_
> ... rootwait modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:20 g_ether.dev_addr=00:22:82:ff:ff:22 ...

---

# Bootup the Pi for installation

_If connecting via OTG, connect a USB cable to the USB port only_
_(that will power the Pi and enable connection)_

## Login to via ssh

> ssh pi@raspberrypi.local

### Copy `rc.local` into /etc

### Copy `start_pi_stream` to `/home/pi`

### Copy install.sh to `/home/pi`

### Perform update and installation

> cd /home/pi
> bash install.sh

## Enable the camera on the Pi:

>raspi-config

* Select: Interfacing Options
* Select: Camera
* Select: Yes

Once configured, there will be a prompt to reboot. Perform the reboot.


---
# After setup and installation

## GStreamer on the Pi:

_start_pi_stream_
```bash
DEST_IP=10.42.0.1 # IP of PC when connected to Pi via USB OTG

gst-launch-1.0 -v rpicamsrc num-buffers=-1 ! video/x-raw,width=640,height=480, framerate=30/1 ! timeoverlay time-mode="buffer-time" ! jpegenc !  rtpjpegpay !  udpsink host=DEST_IP port=5001
```

## GStreamer on the PC

_consume_pi_stream_
```bash
gst-launch-1.0 udpsrc port=5001 ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink
```

## Consume the stream with an SDP file

_More debugging is needed for this to work_

> vlc stream.sdp

_However, this does work..._
```python
import os
import cv2

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"

cap = cv2.VideoCapture('stream.sdp')
while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

```

---

## References:
- https://hackaday.io/project/167996-pi-microscope
- https://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/
- https://www.raspberrypi.org/forums/viewtopic.php?t=213397
- https://www.raspberrypi.org/forums/viewtopic.php?t=171791
- https://en.wikipedia.org/wiki/Session_Description_Protocol
- https://developer.ridgerun.com/wiki/index.php/Introduction_to_network_streaming_using_GStreamer
- http://gstreamer-devel.966125.n4.nabble.com/SDP-file-with-VLC-td4676852.html
---
## Troubleshooting:

_On Ubuntu 18.04, I needed to modify the USB/Ethernet connection as described [here](https://askubuntu.com/questions/1039907/how-to-share-wired-network-connection-in-18-04) and [here](https://raspberrypi.stackexchange.com/questions/73523/connect-pi-zero-via-usb-rndis-gadget-to-ubuntu-17-04)_
- Open nmtui
- Edit connection (Wired connection 1)
- Set IPv4 to "Link Local Only"
    - To share internet, select "Shared to other computers"
