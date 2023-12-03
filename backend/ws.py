import asyncio
import websockets
import json
import game
import threading
from datetime import datetime


async def handler(websocket):
    while True:
        state = game.state
        message = json.dumps(state)
        await asyncio.sleep(0.01)
        await websocket.send(message)


async def main():
    server = await websockets.serve(handler, '', 3389)
    await server.wait_closed()

if __name__ == "__main__":
    game_thread = threading.Thread(target=game.start_game)
    game_thread.daemon = True
    game_thread.start()
    asyncio.run(main())
