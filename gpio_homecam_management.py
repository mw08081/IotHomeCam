from flask import Flask, render_template, Response
from picamera2 import Picamera2
import io
import time

def init_camera():
    global camera
    if camera is None:
        camera = Picamera2()

        camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
        camera.start()