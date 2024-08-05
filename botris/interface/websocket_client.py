import asyncio

import websockets


class WebSocketClient:
    def __init__(self, url, message_handler):
        self.url = url
        self.message_handler = message_handler

    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            await self.handle_connection(websocket)

    async def handle_connection(self, websocket):
        async for message in websocket:
            await self.message_handler(message, websocket)
