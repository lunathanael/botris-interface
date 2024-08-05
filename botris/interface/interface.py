from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable

from .handlers import (construct_message_handler,
                       tracker_construct_message_handler)
from .websocket_client import WebSocketClient

if TYPE_CHECKING:
    from bots import Bot

async def connect(token, room_key, bot: Bot, tracking: bool=False) -> Awaitable[None]:
    """
    Connects to the interface using the provided token and room key.

    Parameters:
    --------
    token : str
        The token for authentication.
    room_key : str
        The key for the room.
    bot : Bot
        The bot that will be used for analysis.
    tracking : bool
        A flag indicating whether tracking is enabled.
    """
    itf: Interface = Interface.create(token, room_key, bot, tracking)
    await itf.connect()

class Interface:
    """
    Represents an interface for interacting with a WebSocket client.

    Attributes:
    --------
    token : str
        The token used for authentication.
    room_key : str
        The key for the room.
    url : str
        The URL for the WebSocket client.
    client : WebSocketClient
        The WebSocket client.
    bot : Bot
        The bot that will be used for analysis.
    
    Methods:
    --------
    __init__(self)
        Initializes the Interface class.
    create(cls, token: str, room_key: str, bot: Bot, tracking: bool=False) -> Interface:
        Creates an instance of the Interface class.
    connect(self) -> Awaitable[None]:
        Connects to the WebSocket client.

    """
    def __init__(self):
        """
        Factory method for creating an instance of the Interface class.
        """
        self.token: str = None
        self.room_key: str = None
        self.url: str = None
        self.client: WebSocketClient = None
        self.bot: Bot = None

    @classmethod
    def create(cls, token: str, room_key: str, bot: Bot, tracking: bool=False) -> Interface:
        """
        Creates an instance of the Interface class.

        Parameters:
        --------
        token : str
            The token used for authentication.
        room_key : str
            The key for the room.
        bot : Bot
            The bot that will be used for analysis.
        tracking : bool
            A flag indicating whether tracking is enabled.

        Returns:
        --------
        Interface
            An instance of the Interface class.
        """
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
    
    async def connect(self) -> Awaitable[None]:
        """
        Connects to the WebSocket client.
        """
        await self.bot.start()
        await self.client.connect()
    
    def __del__(self):
        del self.client
        del self.bot
