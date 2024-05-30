from flask import Flask, render_template, Response
from picamera2 import Picamera2
import io
import time
import threading

# 스레드 중지를 위한 플래그
is_homecamStreaming = False
homecam_streaming_thread = None
picam2 = None



# def init_camera():
#     global camera
#     if camera is None:
#         camera = Picamera2()

#         camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
#         camera.start()

def streaming() :
    global picam2

    picam2 = Picamera2()

    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()
    time.sleep(2)

    # Start streaming
    while is_homecamStreaming:  # While streaming flag is True
        try:
            output = io.BytesIO()
            picam2.capture_file(output, format='jpeg')
            output.seek(0)
            frame = output.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error capturing frame: {e}")
    
    # global picam2

    # picam2 = Picamera2()

    # picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    # picam2.start()
    # # preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    # # picam2.configure(preview_config)
    # # picam2.start_preview(Preview.QTGL)
    
    # # picam2.start()
    # time.sleep(2)

    # # Start streaming
    # metadata = picam2.capture_file("stream.jpg")  # Just a placeholder for actual streaming logic
    # # print(metadata)

def prog_exit() : 
    global picam2

    if picam2:
        picam2.stop()
        picam2.close()
        picam2 = None
        print("Camera stopped and closed")

async def start_streaming():
    global is_homecamStreaming, homecam_streaming_thread

    if homecam_streaming_thread is None or not homecam_streaming_thread.is_alive() :
        is_homecamStreaming = True
        homecam_streaming_thread = threading.Thread(target = streaming)
        homecam_streaming_thread.start()

async def stop_streaming():
    global is_homecamStreaming, homecam_streaming_thread

    print('home came streaming stop', homecam_streaming_thread)
    if homecam_streaming_thread is not None : 
        is_homecamStreaming = False
        
        prog_exit()
        homecam_streaming_thread.join(timeout = 5)
        
        if homecam_streaming_thread.is_alive():
            print("스레드가 제시간에 종료되지 않았습니다.")
        else:
            print("스레드가 성공적으로 종료되었습니다.")