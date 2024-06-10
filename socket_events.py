from common import get_system_info, sio  # common.py에서 get_system_info 함수, sio 변수를 가져옵니다.

from gpio_3_color_led import start_rgb_3color_leds, stop_rgb_3color_leds, rgb_3color_leds_state
from gpio_homecam_management import start_streaming, stop_streaming, get_is_streaming
from gpio_temperature import start_temperature

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


@sio.on('set_3color_led')
async def on_set_3color_led(sid, data):
    print("set_3color_led", sid, data)
    if data['data'] == 'on':
        await start_rgb_3color_leds()
    elif data['data'] == 'off':
        print("led 스위치 off", sid, data)
        await stop_rgb_3color_leds()

    # 이거 안보내도 될거같은데;;
    # data['state'] = await rgb_3color_leds_state()
    # await sio.emit('ret_3color_led', data, room=sid)

@sio.on('get_3color_led')
async def on_get_3color_led(sid, data):
    data['state'] = await rgb_3color_leds_state()
    await sio.emit('ret_3color_led', data, room=sid)


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
    # await sio.emit('ret_homecam_active', data, room=sid)
    # if (data['state']) :
    #     await start_streaming(sio, sid)

@sio.on('get_temperature')
async def on_get_temperature(sid, data):
    await start_temperature(sio, sid)
    #data['state'] = await temperature_state()