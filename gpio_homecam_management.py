# from flask import Flask, render_template, Response
from picamera2 import Picamera2
import io
import time
import threading
import asyncio

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

def streaming(sio, sid) :
    global picam2, is_homecamStreaming, loop

    picam2 = Picamera2()

    picam2.resolution = (1920, 1080)
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    
    picam2.start()
    time.sleep(2)

    # Start streaming
    while is_homecamStreaming:  # While streaming flag is True
        # time.sleep(0.1) 
        # try:
        #     loop = asyncio.new_event_loop()
        #     asyncio.set_event_loop(loop)
        #     try:
        #         loop.run_until_complete(send_img_data(sio, sid))
        #     finally:
        #         loop.close()
        try:
                loop.run_until_complete(send_img_data(sio, sid))
        except Exception as e:
            print(f"Error capturing frame: {e}")
        # finally:
        #         loop.close()

    print("thread out")
    

def prog_exit() : 

    global picam2
    print("prog exit ", picam2)

    if picam2:
        picam2.stop()
        picam2.close()
        picam2 = None
        print("Camera stopped and closed ", picam2 is None)

async def start_streaming(sio, sid):
    global is_homecamStreaming, homecam_streaming_thread, loop

    if homecam_streaming_thread is None or not homecam_streaming_thread.is_alive() :
        is_homecamStreaming = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        homecam_streaming_thread = threading.Thread(target = streaming, args=(sio, sid))
        homecam_streaming_thread.start()
    elif is_homecamStreaming == True and homecam_streaming_thread is not None :
        pass

async def stop_streaming():
    global is_homecamStreaming, homecam_streaming_thread
    
    if homecam_streaming_thread is not None : 
        is_homecamStreaming = False
        
        prog_exit()
        homecam_streaming_thread.join(timeout = 5)
        
        if homecam_streaming_thread.is_alive():
            print("스레드가 제시간에 종료되지 않았습니다.")
        else:
            print("스레드가 성공적으로 종료되었습니다.")

async def get_is_streaming() :
    global is_homecamStreaming
    return is_homecamStreaming