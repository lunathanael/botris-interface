import random
from typing import Dict, List, Literal, Optional, Tuple
from functools import lru_cache

from .models import PIECES, Block, Piece

PieceMatrix = Tuple[Tuple[Optional[Piece]]]

PIECE_MATRICES: Dict[Piece, PieceMatrix] = {
    "Z": (
        ("Z", "Z", None),
        (None, "Z", "Z"),
        (None, None, None)
    ),
    "L": (
        (None, None, "L"),
        ("L", "L", "L"),
        (None, None, None)
    ),
    "O": (
        ("O", "O"),
        ("O", "O")
    ),
    "S": (
        (None, "S", "S"),
        ("S", "S", None),
        (None, None, None)
    ),
    "I": (
        (None, None, None, None),
        ("I", "I", "I", "I"),
        (None, None, None, None),
        (None, None, None, None)
    ),
    "J": (
        ("J", None, None),
        ("J", "J", "J"),
        (None, None, None)
    ),
    "T": (
        (None, "T", None),
        ("T", "T", "T"),
        (None, None, None)
    ),
}


def rotate_matrix(matrix: PieceMatrix, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    for _ in range(rotation):
        matrix = list(zip(*matrix[::-1]))
    return tuple(tuple(row) for row in matrix)


def _get_piece_matrix(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    return rotate_matrix(PIECE_MATRICES[piece], rotation)


FAST_PIECE_MATRICES: Tuple[Tuple[PieceMatrix]] = tuple(
    tuple(
        _get_piece_matrix(piece, rotation)
        for rotation in range(4)
    )
    for piece in PIECES
)

@lru_cache(None)
def get_matrix_mask(board: Tuple[Tuple[Optional[Block]]]) -> int:
    return sum(
        1 << (y * 3 + x)
        for y, row in enumerate(board)
        for x, cell in enumerate(row)
        if cell is not None
    )

FAST_PIECE_MASKS: Tuple[Tuple[int]] = tuple(
    tuple(
        get_matrix_mask(FAST_PIECE_MATRICES[piece_index][rotation])
        for rotation in range(4)
    )
    for piece_index, _ in enumerate(PIECES)
)

WALLKICK = Tuple[Tuple[int, int]]


_WALLKICKS: Dict[str, WALLKICK] = {
    "0-1": ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    "1-0": ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    "1-2": ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    "2-1": ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    "2-3": ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
    "3-2": ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    "3-0": ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    "0-3": ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
}

_I_WALLKICKS: Dict[str, WALLKICK] = {
    "0-1": ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
    "1-0": ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
    "1-2": ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
    "2-1": ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
    "2-3": ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
    "3-2": ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
    "3-0": ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
    "0-3": ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
}

WALLKICKS: Tuple[Tuple[Optional[WALLKICK]]] = tuple(
    tuple(
        _WALLKICKS[f"{i}-{j}"] if (i + j) % 2 == 1 else None
        for j in range(4)
    )
    for i in range(4)
)

I_WALLKICKS: Tuple[Tuple[Optional[WALLKICK]]] = tuple(
    tuple(
        _I_WALLKICKS[f"{i}-{j}"] if (i + j) % 2 == 1 else None
        for j in range(4)
    )
    for i in range(4)
)

def generate_bag() -> List[Piece]:
    bag = list(PIECES)
    random.shuffle(bag)
    return bag

PIECE_INDEX_MAP = {piece: PIECES.index(piece) for i, piece in enumerate(PIECES)}

def get_piece_matrix(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    piece_index: int = PIECE_INDEX_MAP[piece]
    return FAST_PIECE_MATRICES[piece_index][rotation]

def get_piece_mask(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> int:
    piece_index: int = PIECE_INDEX_MAP[piece]
    # print(get_piece_matrix(piece, rotation))
    # print(FAST_PIECE_MASKS[piece_index][rotation])
    return FAST_PIECE_MASKS[piece_index][rotation]