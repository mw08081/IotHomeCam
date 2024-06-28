from common import get_system_info, sio  # common.py에서 get_system_info 함수, sio 변수를 가져옵니다.

from gpio_3_color_led import start_rgb_3color_leds, stop_rgb_3color_leds, rgb_3color_leds_state
from gpio_homecam_management import start_streaming, stop_streaming, ret_start_record, get_is_streaming
from gpio_wallpad_open import open_wallpad
from gpio_temperature import start_temperature
from gpio_light_control import Manage_light_manually, Manage_lightingSystem_mechanism

@sio.event
async def connect(sid, environ):
    print('클라이언트 연결', sid)
@sio.event
async def disconnect(sid):
    print('클라이언트 종료', sid)
@sio.on('get_system_info')
async def on_get_system_info(sid, data):
    systemInfo = get_system_info()
    await sio.emit('ret_system_info', systemInfo, room=sid)

@sio.on('set_homecam_state')
async def on_set_homecam_state(sid, data):
    print("set_homecam_State", sid, data)
    if data['data'] == 'on':
        print(sid, data)
        await start_streaming(sio, sid)
    elif data['data'] == 'off':
        await stop_streaming()

@sio.on('get_homecam_state')
async def on_get_homecam_state(sid, data):
    data['state'] = await get_is_streaming()
    print(data)
    await sio.emit('set_homecam_switch_state', data, room=sid)

@sio.on('ret_camera_recording_start')
async def on_ret_camera_recording_start(sid):
    await ret_start_record()




@sio.on('ret_wallpad_open')
async def on_ret_wallpad_open(sid):
    await open_wallpad()

@sio.on('get_temperature')
async def on_get_temperature(sid, data):
    await start_temperature(sio, sid)

@sio.on('set_lightingSystem_mechanism')
async def on_set_lightingSystem_mechanism(sid, data):
    print("set_lightingSystem_mechanism", sid, data)
    await Manage_lightingSystem_mechanism(data)

@sio.on('set_light_state')
async def on_set_light_state(sid, data):
    print("set_light_state", sid, data)
    await Manage_light_manually(data)
    