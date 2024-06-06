#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import time
import io
from picamera2 import Picamera2, Preview

 picam2 = Picamera2()

picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
time.sleep(2)

output = io.BytesIO()
picam2.capture_file(output, format='jpeg')
output.seek(0)
frame = output.read()

print(type(output))
print(type(frame))




# picam2.start_preview(Preview.QTGL)
# metadata = picam2.capture_file("test.jpg")
# print(metadata)

# picam2.close()
picam2.stop()
picam2.close()