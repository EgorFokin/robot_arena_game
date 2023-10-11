import asyncio
import websockets
import json
import game
import threading


async def handler(websocket, path):
    try:
        while True:
            message = json.dumps(game.players)
            await websocket.send(message)
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosedError:
        pass

async def main():
    server = await websockets.serve(handler, 'localhost', 8765)
    await server.wait_closed()

if __name__ == "__main__":
    game_thread = threading.Thread(target=game.start_game)
    game_thread.daemon = True
    game_thread.start()
    asyncio.run(main())

    