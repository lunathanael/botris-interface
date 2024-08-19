"""
botris
=====

Provides
  1. An interface to interact with the botris game server.
  2. Comprehensive Tetris engine with customizable options.
  3. Fast available backend for compiled C++ game engine.

How to use the documentation
----------------------------
Documentation is available in docstrings provided
with the code.

We recommend exploring the docstrings using
`IPython <https://ipython.org>`_, an advanced Python shell with
TAB-completion and introspection capabilities.  See below for further
instructions.

The docstring examples assume that `botris` has been imported as ``botris``::

  >>> import botris as botris

Code snippets are indicated by three greater-than signs::

  >>> x = 42
  >>> x = x + 1

Use the built-in ``help`` function to view a function's docstring::

  >>> help(botris.core.CGame)

Available subpackages
---------------------
core
    Core ShakTris based game engine.
bots
    Bots for the game engine, also the base class for `Bot`.
engine
    The game engine, `TetrisGame`.
interface
    Interface to interact with the botris game server.

Utilities
---------
__version__
    NumPy version string

Copies vs. References and in-place operations
-----------------------------
Most of the functions in `botris.engine` return a copy of the object referenced.
Most of the functions in `botris.core` return a copy of the object referenced,
specifically containers that dont support indices assignment.
Exceptions to this rule are documented.

Quick Start
-----------
An example to connect to the server with the provided random bot:
    
    >>> import asyncio
    >>> from botris.interface import connect
    >>> from botris.bots import RandomBot
    >>> async def main():
    ...     interface = await connect(
    ...                     "TOKEN",
    ...                     "ROOM_KEY",
    ...                     RandomBot()
    ...                 )
    ...
    >>> asyncio.run(main())
"""

from . import bots, core, engine, interface
from ._version import __version__
from .engine import TetrisGame
from .interface import Interface, connect

__all__ = [
    "bots",
    "core",
    "engine",
    "interface",
    "Interface",
    "connect",
    "TetrisGame",
    "__version__",
]
