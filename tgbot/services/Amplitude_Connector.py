import aiohttp
import json

from tgbot.config import load_config

config = load_config()

async def Amplitude_Logger(exported_data : dict):
    endpoint = 'https://api2.amplitude.com/2/httpapi'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }
    data = {
        "api_key" : config.misc.amplitude_Token,
        "events" : [exported_data]
    }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            print('Amplitude post.')
            return await response.json()