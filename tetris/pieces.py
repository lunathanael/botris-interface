# pieces.py

import random

PIECES = ['I', 'O', 'J', 'L', 'S', 'Z', 'T']

PIECE_MATRICES = {
    "Z": [
        ["Z", "Z", None],
        [None, "Z", "Z"],
        [None, None, None]
    ],
    "L": [
        [None, None, "L"],
        ["L", "L", "L"],
        [None, None, None]
    ],
    "O": [
        ["O", "O"],
        ["O", "O"]
    ],
    "S": [
        [None, "S", "S"],
        ["S", "S", None],
        [None, None, None]
    ],
    "I": [
        [None, None, None, None],
        ["I", "I", "I", "I"],
        [None, None, None, None],
        [None, None, None, None]
    ],
    "J": [
        ["J", None, None],
        ["J", "J", "J"],
        [None, None, None]
    ],
    "T": [
        [None, "T", None],
        ["T", "T", "T"],
        [None, None, None]
    ],
}

WALLKICKS = {
    "0-1": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "1-0": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "1-2": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "2-1": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "2-3": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "3-2": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "3-0": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "0-3": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

I_WALLKICKS = {
    "0-1": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "1-0": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "1-2": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "2-1": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "2-3": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "3-2": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "3-0": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "0-3": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}

def generate_bag():
    bag = PIECES.copy()
    random.shuffle(bag)
    return bag

def rotate_matrix(matrix, rotation):
    for _ in range(rotation):
        matrix = list(zip(*matrix[::-1]))
    return [list(row) for row in matrix]

def get_piece_matrix(piece, rotation):
    return rotate_matrix(PIECE_MATRICES[piece], rotation)