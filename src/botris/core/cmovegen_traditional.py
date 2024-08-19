from typing import TYPE_CHECKING

from .cboard import CBoard
from .cconstants import CPieceType
from .cpiece import CPiece


def sky_piece_movegen(board: CBoard, piece_type: CPieceType) -> list[CPiece]:
    """
    Generate the moves for a sky piece.
    Movegen for a convex board with free movement at the top. (Decided by board height of 16 or lower)

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


def convex_movegen(board: CBoard, piece_type: CPieceType) -> list[CPiece]:
    """
    Generate the moves for a convex piece.
    Movegen for if the board is convex and the height is 17 or higher.

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
    from botris._core.traditional_movegen import convex_movegen, sky_piece_movegen

    sky_piece_movegen = sky_piece_movegen
    convex_movegen = convex_movegen

__all__ = [
    "sky_piece_movegen",
    "convex_movegen",
]
