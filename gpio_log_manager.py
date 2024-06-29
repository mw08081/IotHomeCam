import io
import time
from datetime import datetime
import threading
import asyncio
import os


async def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f'Error: File {file_path} not found')
        return ''

async def refresh_log(sio, sid):
    log_file_path = '/home/pi/iot/iot/LogFile/log.txt'

    # log.txt 파일 읽기
    data = await read_log_file(log_file_path)

    await sio.emit('get_log_data', data, room = sid)
