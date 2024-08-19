import asyncio
import json
from threading import Event, Thread
from typing import Awaitable, Optional

import websockets

from .models import SessionId


class WebSocketClient:
    def __init__(self, url, message_handler, threading=False, daemon=True):
        self.url = url
        self.message_handler = message_handler
        self.threading = threading
        self.daemon = daemon

        self.authenticated = Event()
        self.session_id: Optional[SessionId] = None
        self.thread = None

    def thread_connect(self) -> Awaitable[None]:
        asyncio.run(self.handle_connection())

    async def connect(self) -> Optional[SessionId]:
        self.authenticated.clear()
        self.session_id = None
        if self.threading:
            self.thread = Thread(target=self.thread_connect, daemon=self.daemon)
            self.thread.start()
            self.authenticated.wait()
            return self.session_id
        else:
            await self.handle_connection()
            return self.session_id

    async def handle_connection(self):
        async with websockets.connect(self.url) as self.websocket:
            try:
                async for message in self.websocket:
                    if not self.authenticated.is_set():
                        data = json.loads(message)
                        message_type = data.get("type")

                        if message_type == "authenticated":
                            self.session_id = SessionId(data["payload"]["sessionId"])
                            print(
                                f"Authenticated to WebSocket client with session ID: {self.session_id}"
                            )
                            self.authenticated.set()
                    await self.message_handler(message, self.websocket)
            except websockets.exceptions.ConnectionClosed:
                self.websocket = None
                pass
            finally:
                await self.close()

    async def send(self, message):
        await self.websocket.send(message)

    async def close(self):
        if self.websocket:
            # await self.websocket.close()
            self.websocket = None
        self.authenticated.set()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.close())
        except Exception:
            asyncio.run(self.close())
