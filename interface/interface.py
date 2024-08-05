from __future__ import annotations

from typing import TYPE_CHECKING

from .handlers import (construct_message_handler,
                       tracker_construct_message_handler)
from .websocket_client import WebSocketClient

if TYPE_CHECKING:
    from bots import Bot

async def connect(token, room_key) -> Interface:
    return Interface.create(token, room_key)

class Interface:
    def __init__(self):
        self.token: str = None
        self.room_key: str = None
        self.url: str = None
        self.client: WebSocketClient = None
        self.bot: Bot = None

    @classmethod
    def create(cls, token: str, room_key: str, bot: Bot, tracking: bool=False) -> Interface:
        self: Interface = cls()
        self.token = token
        self.room_key = room_key
        self.url = f"wss://botrisbattle.com/ws?token={token}&roomKey={room_key}"
        
        self.bot = bot
        if tracking:
            handle_message = tracker_construct_message_handler(self.bot.analyze)
        else:
            handle_message = construct_message_handler(self.bot.analyze)

        self.client = WebSocketClient(self.url, handle_message)
        return self
    
    async def connect(self):
        await self.bot.start()
        await self.client.connect()
        print("connected")
    
    def __del__(self):
        del self.client
        del self.bot
