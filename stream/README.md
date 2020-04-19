# Start stream on raspberry pi
    - ssh pi@raspberrypi.local
    - python3 stream/stream.py

# Open stream locally
    - vlc tcp/h264://raspberrypi.local:8001

---

References:
https://picamera.readthedocs.io/en/release-1.9/recipes1.html#recording-to-a-network-stream
