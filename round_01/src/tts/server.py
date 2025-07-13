import websockets
import asyncio
import typing
import json
import logging
import subprocess

logger = logging.getLogger("websocket_server")
process = None

async def exception_handeler(handler: typing.Callable):
    """Handle exceptions"""
    try:
        await handler()
    except websockets.ConnectionClosedOK:
        logger.info(f"[Server Closed Ok]")
    except websockets.ConnectionClosedError as e:
        logger.info(f"[Server Closed Error]: {e}")
        logger.debug(e)

async def handler(socket: websockets.WebSocketServerProtocol):
    """Hello handler"""
    async for message in socket:
        if process is not None:
            process.stdin.write(f"{message}\n") 
            process.stdin.flush()
        else:
            logger.warning(f"[No TTS Process Found]")
        print(message)

async def server():
    global process
    process = subprocess.Popen(
        ['./scripts/input_to_speech.sh'],
        # ['cat'],
        stdin=subprocess.PIPE,
        text=True
    )
    async with websockets.serve(lambda socket: exception_handeler(lambda: handler(socket)), "", 8001):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            process.stdin.close()
            logging.info("[Canceling Server Process]")

if __name__=="__main__":
    log_file = 'tts.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s: %(message)s')
    asyncio.run(server())
