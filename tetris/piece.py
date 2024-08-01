from typing import List, Tuple

class Piece:
    I = 'I'
    O = 'O'
    J = 'J'
    L = 'L'
    S = 'S'
    Z = 'Z'
    T = 'T'

    @classmethod
    def all_pieces(cls) -> List[str]:
        return [cls.I, cls.O, cls.J, cls.L, cls.S, cls.Z, cls.T]

class PieceData:
    def __init__(self, piece: str, x: int, y: int, rotation: int):
        self.piece = piece
        self.x = x
        self.y = y
        self.rotation = rotation

PIECE_MATRICES = {
    Piece.Z: [
        ["Z", "Z", None],
        [None, "Z", "Z"],
        [None, None, None]
    ],
    Piece.L: [
        [None, None, "L"],
        ["L", "L", "L"],
        [None, None, None]
    ],
    Piece.O: [
        ["O", "O"],
        ["O", "O"]
    ],
    Piece.S: [
        [None, "S", "S"],
        ["S", "S", None],
        [None, None, None]
    ],
    Piece.I: [
        [None, None, None, None],
        ["I", "I", "I", "I"],
        [None, None, None, None],
        [None, None, None, None]
    ],
    Piece.J: [
        ["J", None, None],
        ["J", "J", "J"],
        [None, None, None]
    ],
    Piece.T: [
        [None, "T", None],
        ["T", "T", "T"],
        [None, None, None]
    ]
}

WALL_KICKS = {
    "0-1": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "1-0": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "1-2": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "2-1": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "2-3": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "3-2": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "3-0": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "0-3": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
}

I_WALL_KICKS = {
    "0-1": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "1-0": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "1-2": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "2-1": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "2-3": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "3-2": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "3-0": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "0-3": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
}