from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Optional

from .handlers import construct_message_handler, tracker_construct_message_handler
from .models import SessionId
from .websocket_client import WebSocketClient

if TYPE_CHECKING:
    from bots import Bot


async def connect(
    token,
    room_key,
    bot: Bot,
    tracking: bool = False,
    threading: bool = False,
    daemon: bool = True,
) -> Awaitable[Interface]:
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
    threading : bool
        A flag indicating whether to use threading.
    daemon : bool
        A flag indicating whether to use daemon threading or normal threading.

    Returns:
    --------
    Awaitable[Interface]
        An instance of the Interface class.
    """
    itf: Interface = Interface.create(token, room_key, bot, tracking, threading, daemon)
    await itf.connect()
    return itf


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
    daemon : bool
        A flag indicating whether to use daemon threading or normal threading.
    status : str
        The current status of the interface.

    Methods:
    --------
    __init__(self, daemon: bool = False)
        Initializes the Interface class.
    create(cls, token: str, room_key: str, bot: Bot, tracking: bool = False, daemon: bool = False) -> Interface:
        Creates an instance of the Interface class.
    connect(self) -> Awaitable[None]:
        Connects to the WebSocket client.
    close(self) -> None:
        Closes the WebSocket client.
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
        self.threading: bool = None
        self.daemon: bool = None
        self.status: str = None
        self.session_id: SessionId = None

    @classmethod
    def create(
        cls,
        token: str,
        room_key: str,
        bot: Bot,
        tracking: bool = False,
        threading: bool = False,
        daemon: bool = True,
    ) -> Interface:
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
        tracking : bool, optional
            A flag indicating whether tracking is enabled. Default is False.
        threading : bool, optional
            A flag indicating whether to use threading. Default is False.
        daemon : bool, optional
            A flag indicating whether to use daemon threading or normal threading. Default is False.

        Returns:
        --------
        Interface
            An instance of the Interface class.
        """
        self: Interface = cls()
        self.token = token
        self.room_key = room_key
        self.url = f"wss://botrisbattle.com/ws?token={token}&roomKey={room_key}"
        self.threading = threading
        self.daemon = daemon
        self.status = "disconnected"

        self.bot = bot
        if tracking:
            handle_message = tracker_construct_message_handler(self.bot.analyze)
        else:
            handle_message = construct_message_handler(self.bot.analyze)

        self.client = WebSocketClient(
            self.url, handle_message, threading=self.threading, daemon=self.daemon
        )
        return self

    async def connect(self) -> Awaitable[None]:
        """
        Connects to the WebSocket client and bot.
        """
        await self.bot.start()

        self.status = "connecting"
        session_id: SessionId | None = await self.client.connect()
        if session_id is None:
            self.status = "disconnected"
            raise Exception("Failed to connect to WebSocket client!")

        self.status = "connected"
        self.session_id = session_id

    async def close(self) -> None:
        """
        Closes the WebSocket client and bot.
        """
        await self.client.close()
        self.bot.shutdown()

    def __del__(self):
        del self.client
        del self.bot
