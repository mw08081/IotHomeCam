
from common import response_html

async def mainHandle(request):
    return response_html('index.html')

async def video_feed(request):
    return response_html('homecam.html')


async def temperatureHandle(request):
    return response_html('temperature.html')





async def managementHandle(request):
    return response_html('management.html')

async def loginHandle(request):
    return response_html('login.html')

    #html 을 만들어서 핸들러를 하나씩 붙이면 된다는데..