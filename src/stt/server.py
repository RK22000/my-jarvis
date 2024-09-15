import websockets
import asyncio
import typing
import speech_to_text
import json
import logging
logger = logging.getLogger("websocket_server")

async def exception_handeler(handler: typing.Callable):
    """Handle exceptions"""
    try:
        await handler()
    except websockets.ConnectionClosedOK:
        logger.info("[Server Closed Ok]")
    except websockets.ConnectionClosedError as e:
        logger.info(f"[Server Closed Error]: {e}")
        logger.debug(e)

async def handler(socket: websockets.WebSocketServerProtocol):
    """Hello handler"""
    while True:
        for results in speech_to_text.generate_STT():
            await socket.send(json.dumps(results))
        # await socket.send("Hello")
        # await asyncio.sleep(1)

async def server():
    async with websockets.serve(lambda socket: exception_handeler(lambda: handler(socket)), "", 8001):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("[Canceling Server Process]")

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(server())
