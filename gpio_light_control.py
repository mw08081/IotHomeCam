#gpio_3_color_led.py
import RPi.GPIO as GPIO
import time
import threading

# 핀 번호 설정


# GPIO 핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀의 모드를 출력으로 설정


# 스레드 중지를 위한 플래그
is_pir_running = False
pir_thread = None

async def start_pir_sensor() :
    print("pir started ")


# async def Reigst():
#     # pir 이벤트 등록
#     global rgb_3color_led_thread, is_rgb_3color_led
#     if rgb_3color_led_thread is None or not rgb_3color_led_thread.is_alive():
#         is_rgb_3color_led = True
#         rgb_3color_led_thread = threading.Thread(target=cycle_rgb_3color_leds)
#         rgb_3color_led_thread.start()

# async def stop_rgb_3color_leds():
#     global rgb_3color_led_thread, is_rgb_3color_led
   
#     print("pir 이벤트 해제")
#     if rgb_3color_led_thread is not None:
#         is_rgb_3color_led = False
#         rgb_3color_led_thread.join(timeout=5)  # 5초 후에 강제 종료
#         if rgb_3color_led_thread.is_alive():
#             print("스레드가 제시간에 종료되지 않았습니다.")
#         else:
#             print("스레드가 성공적으로 종료되었습니다.")

# async def rgb_3color_leds_state():
#     global is_rgb_3color_led
#     return is_rgb_3color_led