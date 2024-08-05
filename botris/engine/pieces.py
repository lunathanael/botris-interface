import random
from itertools import product
from typing import Dict, List, Literal, Optional, Tuple

from .models import PIECES, Piece, _Piece

PieceMatrix = Tuple[Tuple[Optional[Piece]]]

PIECE_MATRICES: Dict[_Piece, PieceMatrix] = {
    "Z": (("Z", "Z", None), (None, "Z", "Z"), (None, None, None)),
    "L": ((None, None, "L"), ("L", "L", "L"), (None, None, None)),
    "O": (("O", "O"), ("O", "O")),
    "S": ((None, "S", "S"), ("S", "S", None), (None, None, None)),
    "I": (
        (None, None, None, None),
        ("I", "I", "I", "I"),
        (None, None, None, None),
        (None, None, None, None),
    ),
    "J": (("J", None, None), ("J", "J", "J"), (None, None, None)),
    "T": ((None, "T", None), ("T", "T", "T"), (None, None, None)),
}


def rotate_matrix(matrix: PieceMatrix, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    for _ in range(rotation):
        matrix = list(zip(*matrix[::-1]))
    return tuple(tuple(row) for row in matrix)


def _get_piece_matrix(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    return rotate_matrix(PIECE_MATRICES[piece.value], rotation)


FAST_PIECE_MATRICES: Tuple[Tuple[PieceMatrix]] = tuple(
    tuple(_get_piece_matrix(piece, rotation) for rotation in range(4))
    for piece in PIECES
)


def _get_matrix_mask(board: Tuple[Tuple[bool]]) -> int:
    return sum(1 << (y * 4 + x) for y in range(4) for x in range(4) if board[y][x])


def _get_piece_mask(piece_index: int, rotation: Literal[0, 1, 2, 3]) -> int:
    mask: int = 0

    piece_matrix: PieceMatrix = FAST_PIECE_MATRICES[piece_index][rotation]
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell is not None:
                board_x = 0 + piece_x
                board_y = 3 - piece_y
                mask |= 1 << (board_y * 4 + board_x)
    return mask


FAST_PIECE_MASKS: Tuple[Tuple[int]] = tuple(
    tuple(_get_piece_mask(piece_index, rotation) for rotation in range(4))
    for piece_index, _ in enumerate(PIECES)
)


def _get_piece_border(
    piece_index: int, rotation: Literal[0, 1, 2, 3]
) -> Tuple[Tuple[int]]:
    lowest_x = 3
    highest_x = 0
    lowest_y = 3
    highest_y = 0

    piece_matrix: PieceMatrix = FAST_PIECE_MATRICES[piece_index][rotation]
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell is not None:
                lowest_x = min(lowest_x, piece_x)
                highest_x = max(highest_x, piece_x)
                lowest_y = min(lowest_y, piece_y)
                highest_y = max(highest_y, piece_y)

    return lowest_x, highest_x, lowest_y, highest_y


PIECE_BORDERS: Tuple[Tuple[Tuple[int]]] = tuple(
    tuple(_get_piece_border(piece_index, rotation) for rotation in range(4))
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
    tuple(_WALLKICKS[f"{i}-{j}"] if (i + j) % 2 == 1 else None for j in range(4))
    for i in range(4)
)

I_WALLKICKS: Tuple[Tuple[Optional[WALLKICK]]] = tuple(
    tuple(_I_WALLKICKS[f"{i}-{j}"] if (i + j) % 2 == 1 else None for j in range(4))
    for i in range(4)
)


def generate_bag() -> List[Piece]:
    bag = list(PIECES)
    random.shuffle(bag)
    return bag


def get_piece_matrix(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> PieceMatrix:
    return FAST_PIECE_MATRICES[piece.index][rotation]


def get_piece_mask(piece: Piece, rotation: Literal[0, 1, 2, 3]) -> int:
    return FAST_PIECE_MASKS[piece.index][rotation]


def get_piece_border(
    piece: Piece, rotation: Literal[0, 1, 2, 3]
) -> Tuple[int, int, int, int]:
    return PIECE_BORDERS[piece.index][rotation]
