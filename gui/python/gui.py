'''
Inspired by:
https://gist.github.com/ExpandOcean/de261e66949009f44ad2
'''

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
import cv2
import os
from datetime import datetime

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(BASE, 'images')


class MicroscopeCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(MicroscopeCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.started = True

    def update(self, dt):
        if self.started:
            ret, frame = self.capture.read()
            if ret:
                # convert it to texture
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(
                    buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.texture = image_texture

    def pause_camera(self):
        self.started = False

    def start_camera(self):
        if not self.started:
            self.started = True

    def capture_image(self):
        ret, frame = self.capture.read()
        if ret:
            timestamp = int(datetime.now().timestamp())
            img_name = f"microscope_{timestamp}.png"
            print(f"Capturing: {img_name}")
            img_name = os.path.join(IMAGES, img_name)
            cv2.imwrite(img_name, frame)


class PauseButton(Button):
    pass


class StartButton(Button):
    pass


class CaptureButton(Button):
    pass


class MicroscopeApp(App):
    def build(self):
        self.capture = cv2.VideoCapture('stream.sdp')
        self.my_camera = MicroscopeCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    MicroscopeApp().run()
