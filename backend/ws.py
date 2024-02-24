import asyncio
import websockets
import json
import game
import threading
from datetime import datetime, timedelta


ip_requests = {}


async def recieve_messages(websocket):
    async for message in websocket:
        data = json.loads(message)
        if data["type"] == "join":
            if data["player_name"] not in game.queue:
                if (not websocket.remote_address[0] in ip_requests):
                    ip_requests[websocket.remote_address[0]] = []
                else:
                    for i in range(len(ip_requests[websocket.remote_address[0]])-1, -1, -1):
                        if (datetime.now() - ip_requests[websocket.remote_address[0]][i]) > timedelta(seconds=30):
                            ip_requests[websocket.remote_address[0]].pop(i)
                ip_requests[websocket.remote_address[0]].append(datetime.now())
                if len(ip_requests[websocket.remote_address[0]]) > 2:
                    continue
                game.queue.append(data["player_name"])


async def send_messages(websocket):
    while True:
        try:
            state = game.state
            state['queue'] = game.queue
            message = json.dumps(state)
            await asyncio.sleep(0.01)
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            del ip_requests[websocket.remote_address[0]]
            break


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
