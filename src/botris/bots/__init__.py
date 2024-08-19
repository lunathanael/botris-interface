"""
This module contains the bot classes that can be used to create Bots to interact with the interface.

Available subpackages
--------------------
bot
    The base class for all bots.
randombot
    An example bot that plays randomly.

An example to create a bot from `Bot` class:

    >>> from botris.bots import Bot
    >>> from botris.interface import Command
    >>> class LeftBot(Bot):
    ...     async def analyze(self):
    ...         return [Command.move_left]
    ...
    >>> bot = LeftBot()
"""

from .bot import Bot
from .randombot import RandomBot

__all__ = ["Bot", "RandomBot"]
