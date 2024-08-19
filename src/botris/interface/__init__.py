"""
This module provides an interface to interact with the botris server.

Available subpackages
--------------------
interface
    Contains the interface class used to interact with the server.
models
    Contains the data models used by the interface.
handlers
    Contains the message handlers used by the interface.
websocket_client
    Contains the websocket client used by the interface.

An example to connect to the server:

    >>> from botris.interface import Interface
    >>> from botris.bots import RandomBot
    >>> async def main():
    ...     interface = await Interface(
    ...                     "TOKEN",
    ...                     "ROOM_KEY",
    ...                     RandomBot()
    ...                 )
    ...

Or using `connect`

    >>> from botris.interface import connect
    >>> from botris.bots import RandomBot
    >>> async def main():
    ...     interface = await connect(
    ...                     "TOKEN",
    ...                     "ROOM_KEY",
    ...                     RandomBot()
    ...                 )
    ...
"""

from . import models
from .handlers import construct_message_handler
from .interface import Interface, connect
from .models import (
    Block,
    Board,
    Command,
    GameState,
    Piece,
    PieceData,
    PlayerData,
    PlayerInfo,
    PublicGarbageLine,
    RoomData,
)
from .websocket_client import WebSocketClient

__all__ = [
    "Interface",
    "connect",
    "models",
    "construct_message_handler",
    "WebSocketClient",
    "Piece",
    "PieceData",
    "PlayerData",
    "PlayerInfo",
    "PublicGarbageLine",
    "Block",
    "Board",
    "GameState",
    "Command",
    "RoomData",
]
