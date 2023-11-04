import asyncio
import websockets
import json
import game
import threading
from datetime import datetime

def on_pause_button_pressed():
    if game.game_active:
        game.pause()
    else:
        game.unpause()

async def recieve_messages(websocket):
    async for message in websocket:
        data = json.loads(message)
        match data["type"]:
            case "button_press":
                match data["content"]:
                    case "start":
                        on_pause_button_pressed()
                    case "reset":
                        game.reset()

async def send_messages(websocket):
    while True:
        state = game.get_state()
        message = json.dumps(state["players"])
        await asyncio.sleep(0.01)
        await websocket.send(message)
        

async def handler(websocket):
    await asyncio.gather(recieve_messages(websocket),send_messages(websocket))

async def main():
    server = await websockets.serve(handler, 'localhost', 8765)
    await server.wait_closed()

if __name__ == "__main__":
    game_thread = threading.Thread(target=game.start_game)
    game_thread.daemon = True
    game_thread.start()
    asyncio.run(main())

    