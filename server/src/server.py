import asyncio, json, websockets

from src import *
from src.clients import Clients, Client
from src.database import database
from src.events import EventHandler

class ChatServer:

    def __init__(self, host, port):
        self.host, self.port = host, port
        self.loop = asyncio.get_event_loop()
        self.clients = Clients()

        self.event_handler = EventHandler(self.clients)

    def run(self):
        self.loop.run_until_complete(self.server())
        self.loop.run_forever()

    async def server(self):
        await websockets.serve(self.handle_client, self.host, self.port)

    async def handle_client(self, ws, path):
        while True:
            try:
                data = await ws.recv()

                if not data:
                    break

                content = json.loads(data)

                t = content.get('type')

                await self.event_handler.handle_event(ws, t, content)

            except Exception as e:
                print(f"Exception: {e}")
                await ws.close()
                break
