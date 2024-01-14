import asyncio
import websockets
import json
import game
import threading
from datetime import datetime


async def recieve_messages(websocket):
    async for message in websocket:
        data = json.loads(message)
        if data["type"] == "join":
            if data["player_name"] not in game.queue:
                game.queue.append(data["player_name"])


async def send_messages(websocket):
    while True:
        state = game.state
        state['queue'] = game.queue
        message = json.dumps(state)
        await asyncio.sleep(0.01)
        await websocket.send(message)


async def handler(websocket):
    await asyncio.gather(recieve_messages(websocket), send_messages(websocket))


async def main():
    server = await websockets.serve(handler, '', 3389)
    await server.wait_closed()

if __name__ == "__main__":
    game_thread = threading.Thread(target=game.start_game)
    game_thread.daemon = True
    game_thread.start()
    asyncio.run(main())
