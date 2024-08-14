import random
from itertools import product
from typing import Dict, List, Literal, Optional, Tuple

import numpy as np
from numba import jit, uint8

from .models import PIECES, Piece, _Piece

PieceMatrix = Tuple[Tuple[Optional[Piece]]]

_PIECE_MATRICES: Dict[_Piece, PieceMatrix] = {
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

PIECE_MATRICES = np.array([
    [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # Z
    [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # L
    [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # O
    [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # S
    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],  # I
    [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # J
    [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # T
], dtype=np.uint8)


@jit(uint8[:,:](uint8[:,:], uint8), nopython=True)
def rotate_matrix(matrix, rotation):
    for _ in range(rotation):
        matrix = np.rot90(matrix, k=3)  # Rotate counterclockwise
    return matrix

@jit(uint8(uint8[:,:]), nopython=True)
def get_matrix_mask(board):
    mask = 0
    for y in range(4):
        for x in range(4):
            if board[y, x]:
                mask |= 1 << (y * 4 + x)
    return mask

@jit(uint8(uint8, uint8), nopython=True)
def get_piece_mask(piece_index, rotation):
    piece_matrix = rotate_matrix(PIECE_MATRICES[piece_index], rotation)
    mask = 0
    for y in range(4):
        for x in range(4):
            if piece_matrix[y, x]:
                board_y = 3 - y
                mask |= 1 << (board_y * 4 + x)
    return mask

@jit(uint8[:](uint8, uint8), nopython=True)
def get_piece_border(piece_index, rotation):
    piece_matrix = rotate_matrix(PIECE_MATRICES[piece_index], rotation)
    lowest_x, highest_x, lowest_y, highest_y = 3, 0, 3, 0
    for y in range(4):
        for x in range(4):
            if piece_matrix[y, x]:
                lowest_x = min(lowest_x, x)
                highest_x = max(highest_x, x)
                lowest_y = min(lowest_y, y)
                highest_y = max(highest_y, y)
    return np.array([lowest_x, highest_x, lowest_y, highest_y], dtype=np.uint8)

FAST_PIECE_MASKS = np.array([[get_piece_mask(p.value, r) for r in range(4)] for p in PIECES], dtype=np.uint8)
PIECE_BORDERS = np.array([[get_piece_border(p.value, r) for r in range(4)] for p in PIECES], dtype=np.uint8)

WALLKICKS = np.array([
    [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
     None,
     [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
     None],
    [None,
     [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
     None,
     [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]],
    [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
     None,
     [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
     None],
    [None,
     [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
     None,
     [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]]
], dtype=object)

I_WALLKICKS = np.array([
    [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
     None,
     [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
     None],
    [None,
     [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
     None,
     [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]],
    [[(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
     None,
     [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
     None],
    [None,
     [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
     None,
     [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]]
], dtype=object)

def generate_bag() -> List[Piece]:
    bag = list(PIECES)
    np.random.shuffle(bag)
    return bag

@jit(np.uint8[:,:](uint8, uint8), nopython=True)
def get_piece_matrix(piece_index, rotation):
    return rotate_matrix(PIECE_MATRICES[piece_index], rotation)

@jit(uint8(uint8, uint8), nopython=True)
def get_piece_mask(piece_index, rotation):
    return FAST_PIECE_MASKS[piece_index, rotation]

@jit(uint8[:](uint8, uint8), nopython=True)
def get_piece_border(piece_index, rotation):
    return PIECE_BORDERS[piece_index, rotation]