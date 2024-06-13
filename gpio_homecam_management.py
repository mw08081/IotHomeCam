from picamera2 import Picamera2
import io
import time
import threading
import asyncio
import RPi.GPIO as GPIO

LED_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# 스레드 중지를 위한 플래그
is_homecamStreaming = False
homecam_streaming_thread = None
picam2 = None
loop = None

async def send_img_data(sio, sid) :
    try : 
        output = io.BytesIO()
        picam2.capture_file(output, format='jpeg')
        output.seek(0)
        frame = output.read()
        await sio.emit('ret_homecam_active', frame, room = sid)
    except Exception as e :
        print(e)

async def streaming(sio, sid) :
    global picam2, is_homecamStreaming, loop

    picam2 = Picamera2()

    picam2.resolution = (1920, 1080)
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    
    picam2.start()
    time.sleep(2)
    GPIO.output(LED_PIN, GPIO.HIGH)

    # Start streaming
    while is_homecamStreaming:  # While streaming flag is True
        try:
            await send_img_data(sio, sid)
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Error capturing frame: {e}")
        # finally:
        #         loop.close()

    print("thread out")
    

def prog_exit() : 
    global picam2

    if picam2:
        picam2.stop()
        picam2.close()
        picam2 = None
        GPIO.output(LED_PIN, GPIO.LOW)
        print("Camera stopped and closed ", picam2 is None)

async def start_streaming(sio, sid):
    global is_homecamStreaming, homecam_streaming_thread, loop

    if not is_homecamStreaming:
        is_homecamStreaming = True
        asyncio.create_task(streaming(sio, sid))
    else:
        print("Streaming is already active")

async def stop_streaming():
    global is_homecamStreaming, homecam_streaming_thread
    
    if is_homecamStreaming : 
        is_homecamStreaming = False
        
        await asyncio.sleep(0.1)
        prog_exit()

async def get_is_streaming() :
    global is_homecamStreaming
    return is_homecamStreaming