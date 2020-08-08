#!/usr/bin/env python

# Inspired by Ben Nuttall's Astro Cam example,
# from: https://github.com/bennuttall/sense-hat-examples/blob/master/python/astro_cam.py
# Written by Dave Jones: https://gist.github.com/waveform80/a2621da13b88c3d751e31a15e97695c2
# Tweaked for Unicorn HAT HD

from signal import pause
from sys import exit
import cv2
import numpy as np

try:
    from picamera import PiCamera
except ImportError:
    exit('This script requires the picamera module\nInstall with: sudo pip install picamera')

from PIL import Image

import unicornhathd


print("""Unicorn HAT HD: Raspberry Pi Camera Display

Show a 16x16 feed from your Raspberry Pi camera!

Press Ctrl+C to exit.

""")

Npixel = 320

class DisplayOutput():
    def __init__(self):
        self.hat = unicornhathd
        self.hat.rotation(90)
        self.hat.brightness(0.6)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def write(self, buf):
        cv_image = np.frombuffer(buf, dtype=np.uint8).reshape([Npixel, Npixel, 3])
        gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            for (x,y,w,h) in faces:
                #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                print(x,y,w,h)
                face = cv_image[y:y+h, x:x+w]
                face = cv2.resize(face, (16,16))
                for x in range(16):
                    for y in range(16):
                        r,g,b = face[y,x]
                        self.hat.set_pixel(x, y, r, g, b)
                self.hat.show()
                break
#        else:
#            img = Image.frombytes('RGB', (Npixel, Npixel), buf)
#            img = img.resize((16, 16), Image.BILINEAR)
#            for x in range(16):
#                for y in range(16):
#                    r, g, b = img.getpixel((x, y))
#                    self.hat.set_pixel(x, y, r, g, b)


with PiCamera() as camera:
    camera.resolution = (Npixel, Npixel)
    camera.contrast = 20
    camera.start_preview()
    output = DisplayOutput()
    camera.start_recording(output, 'rgb')

    try:
        pause()
    finally:
        camera.stop_recording()
        unicornhathd.off()
