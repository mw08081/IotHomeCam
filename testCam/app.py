from flask import Flask, render_template, Response
from picamera2 import Picamera2

import RPi.GPIO as GPIO
import io
import time

app = Flask(__name__)
camera = None
GPIO.setmode(GPIO.BCM)

bPin = 21

def init_camera():
    global camera
    if camera is None:
        camera = Picamera2()

        camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
        camera.start()

        GPIO.setup(bPin, GPIO.OUT)
        GPIO.output(bPin, 1)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global camera
    while True:
        time.sleep(0.01)
        frame = get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_frame():
    global camera
    frame = None
    try:
        output = io.BytesIO()
        camera.capture_file(output, format='jpeg')
        output.seek(0)
        frame = output.read()
    except Exception as e:
        print(f"Error capturing frame: {e}")
    return frame

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init_camera()  # Initialize camera before starting the server
    try:
        app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)  # Disable reloader to avoid double initialization
    finally:
        if camera:
            camera.stop()
            camera.close()
            GPIO.output(bPin, 0)
