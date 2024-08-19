"""
The botris core module provides the python bindings for the core ShakTris based game engine.

Available subpackages
---------------------
cboard
    Contains the board data model used by the engine.
cconstants
    Contains the constants used by the engine.
cgame
    Contains the game data model used by the engine.
cmode
    Contains the mode data model used by the engine.
cmovegen_traditional
    Contains the move generation functions for traditional movegen.
cmovegen_smeared
    Contains the move generation functions for smeared movegen.
"""

from . import cboard, cconstants, cgame, cmode, cmovegen_smeared, cmovegen_traditional
from .cboard import CBoard
from .cconstants import CColorType, CPieceType
from .cgame import CGame
from .cmode import CBotris
from .cmovegen_smeared import god_movegen, movegen
from .cmovegen_traditional import convex_movegen, sky_piece_movegen

__all__ = [
    "cboard",
    "cconstants",
    "cgame",
    "cmode",
    "cmovegen_traditional",
    "cmovegen_smeared",
    "CBoard",
    "CColorType",
    "CPieceType",
    "CGame",
    "CBotris",
    "sky_piece_movegen",
    "convex_movegen",
    "movegen",
    "god_movegen",
]
