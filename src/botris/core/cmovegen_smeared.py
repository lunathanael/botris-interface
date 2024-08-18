from typing import TYPE_CHECKING

from .cconstants import CPieceType
from .cboard import CBoard
from .cpiece import CPiece

def movegen(board: CBoard, piece_type: CPieceType) -> list[CPiece]:
    """
    Generate the moves for a piece.

    Parameters:
    -----------
    board : CBoard
        The board to generate moves for.
    piece_type : CPieceType
        The piece type to generate moves for.

    Returns:
    --------
    list[CPiece]
        The number of moves generated. This is actually of type `VectorPiece`,
        although implementation is similar to `List[Piece]`.
    """
    pass

def god_movegen(board: CBoard, piece_type: CPieceType) -> list[CPiece]:
    """
    Generate the moves for a piece.

    Parameters:
    -----------
    board : CBoard
        The board to generate moves for.
    piece_type : CPieceType
        The piece type to generate moves for.

    Returns:
    --------
    list[CPiece]
        The number of moves generated. This is actually of type `VectorPiece`,
        although implementation is similar to `List[Piece]`.
    """
    pass

if not TYPE_CHECKING:
    from botris._core.smeared_movegen import movegen, god_movegen
    movegen = movegen
    god_movegen = god_movegen

__all__ = [
    "movegen",
    "god_movegen",
]