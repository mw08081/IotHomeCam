import io
import time
import threading
import RPi.GPIO as GPIO
import asyncio

servo_pin = 17

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz (20ms 주기)
pwm.start(0)

is_wallpadOpening = False
wallpad_open_thread = None

def open_wallpad_exec():
    print("open")
    duty = 2 + (90 / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

    time.sleep(1)
    duty = 2 + (0 / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)


async def open_wallpad():
    global is_wallpadOpening, wallpad_open_thread, loop

    if wallpad_open_thread is None or not wallpad_open_thread.is_alive() :
        wallpad_open_thread = threading.Thread(target=open_wallpad_exec)
        wallpad_open_thread.start()