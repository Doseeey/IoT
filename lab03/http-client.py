import requests
import asyncio, aiohttp
import json
import random

async def sendWord(word, integer):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:8080'

        data = {
            'ID': integer, 
            'message': word
        }
        
        await asyncio.sleep(random.randint(0, 3))
        async with session.post(url, json=data):
            print(f"Client {integer} sent {word}")
        

async def main():
    text = "Litwo! Ojczyzno moja! ty jesteś jak zdrowie. Ile cię trzeba cenić, ten tylko się dowie, Kto cię stracił."
    text = text.split()
    coroutines = [sendWord(el, i) for i, el in enumerate(text)]
    await asyncio.gather(*coroutines)

asyncio.run(main())