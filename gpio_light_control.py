import RPi.GPIO as GPIO
import time
import threading

# GPIO 핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀의 모드를 출력으로 설정
LED_PINS = [16,20,21]
# LED 핀의 모드를 출력으로 설정
for pin in LED_PINS :
    GPIO.setup(pin, GPIO.OUT)

# PIR 센서 핀 번호 설정
PIR_PIN = 19
# PIR 핀을 입력으로 설정
GPIO.setup(PIR_PIN, GPIO.IN)
# 사용자가 설정하는 임계값
THRESHOLD = GPIO.HIGH  # 예시로 GPIO.HIGH 값을 임계값으로 설정 (HIGH일 때 트리거)

# 조도센서 핀번호 설정
LR_PIN = 26
# 조도센서 입력으로 설정
GPIO.setup(LR_PIN, GPIO.IN)

# 스레드 중지를 위한 플래그
is_auto = True
is_on = False
pir_thread = None
lr_thread = None


def Manage_Leds(should_on) :
    global LED_PINS, is_auto, is_on
    for pin in LED_PINS :
        GPIO.output(pin, should_on)

    if is_auto and should_on == True:
        time.sleep(5)       # 5초뒤에 끄기
        is_on = False     
        Manage_Leds(False)

def motion_detected():
    print("Motion detected!")
    Manage_Leds(True)               # dn

def Manage_Sensors(should_on):
    global is_on
    #켜야할때
    if should_on :
        #꺼져있다면
        if is_on == False:
            #켜기
            is_on = True
            Manage_Leds(should_on)                                    # pir 등록 대신 생긴부분 : 5초간 led를 켜고 다시 끄는 기능
            # GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)        # pir 이벤트 등록
    #꺼야할때        
    else :
        #켜져있다면
        if is_on == True : 
            #끄기
            is_on = False
            # GPIO.remove_event_detect(PIR_PIN)                                               # pir 이벤트 해제

def handle_lr_sensor_event():
    global is_auto
    while True:             # is_auto 가 false일때 스레드 종료를 방지
        while is_auto : 
            sensor_value = GPIO.input(LR_PIN)
            if sensor_value == THRESHOLD:
                # print("dark")  
                Manage_Sensors(True)
            else :
                pass
                # print("bright")
                # Manage_Sensors(False)
            time.sleep(1)
        time.sleep(2)
    print('thread out')

async def start_sensors() :
    global lr_thread, is_auto

    if lr_thread is None or lr_thread.is_alive() :
        is_auto = True
        lr_thread = threading.Thread(target=handle_lr_sensor_event)
        lr_thread.start()

async def Manage_lightingSystem_mechanism(_isAuto):
    global is_auto, lr_thread
    is_auto = _isAuto

    if(is_auto) :
        Manage_Leds(False)      # isAuto: false/ onOff: true에서 auto로 변경할경우 조명을 모두 제거해야함


async def Manage_light_manually(_shouldOn) :
    global is_on

    # shouldOn 이 True일때
    is_on = _shouldOn           # 불켜짐 true
    Manage_Leds(is_on)          # 값으로 led조작
    