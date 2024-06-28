from picamera2 import Picamera2
import io
import time
from datetime import datetime
import threading
import asyncio
import RPi.GPIO as GPIO


can_record = False
# 스레드 중지를 위한 플래그
is_homecamStreaming = False
picam2 = None

picam2 = Picamera2()

picam2.resolution = (1920, 1080)
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))

picam2.start()
time.sleep(2)

async def ret_start_record():
    global can_record

    if not can_record : 
        can_record = True
        await asyncio.sleep(10)
        can_record = False
    else :
        print('already recording...')

async def recording(frame) :
    try :
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-5]  # 마지막 두 자리(밀리초)를 제외하고 가져옴
        output_file_path = f'/home/pi/iot/iot/LogImg/{current_time}.jpg'
        with open(output_file_path, 'wb') as f:
            f.write(frame)
    except Exception as e :
        print(e)


async def send_img_data(sio, sid) :
    global can_record

    try : 
        output = io.BytesIO()
        picam2.capture_file(output, format='jpeg')
        output.seek(0)
        frame = output.read()

        if can_record :
            await recording(frame)

        await sio.emit('ret_homecam_active', frame, room = sid)
    except Exception as e :
        print(e)

async def streaming(sio, sid) :
    global picam2

    # Start streaming
    while is_homecamStreaming:  # While streaming flag is True
        try:
            await send_img_data(sio, sid)
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Error capturing frame: {e}")

    print("thread out")
 
async def start_streaming(sio, sid):
    global is_homecamStreaming

    if not is_homecamStreaming:
        is_homecamStreaming = True
        asyncio.create_task(streaming(sio, sid))
    else:
        print("Streaming is already active")

def prog_exit() : 
    global picam2

    if picam2:
        picam2.stop()
        picam2.close()
        picam2 = None
        GPIO.output(LED_PIN, GPIO.LOW)
        print("Camera stopped and closed :", picam2 is None)

async def stop_streaming():
    global is_homecamStreaming
    
    if is_homecamStreaming : 
        is_homecamStreaming = False
        
        await asyncio.sleep(0.1)
        # prog_exit()

async def get_is_streaming() :
    global is_homecamStreaming
    return is_homecamStreaming