from . import bots, core, engine, interface
from .engine import TetrisGame
from .interface import Interface, connect
from ._version import __version__

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
