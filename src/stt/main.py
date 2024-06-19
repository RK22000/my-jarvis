import websockets
import asyncio
import json

async def listen():
    async with websockets.connect("ws://localhost:2700") as ws:
        last_rsp = ''
        while True:
            rsp = (await ws.recv())
            rsp = json.loads(rsp)["text"]
            print(rsp)
            # print(rsp) if rsp != "" and last_rsp != "" else None
            last_rsp = rsp
async def make_interuptable(f):
    try:
        await f()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt")

asyncio.run((listen()))