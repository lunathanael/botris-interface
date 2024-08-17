from __future__ import annotations

from dataclasses import asdict, dataclass, field
from sys import intern
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple

if TYPE_CHECKING:
    from botris.interface.models import Command


@dataclass
class GarbageLine:
    delay: int
    index: int

    def public(self) -> dict[str, int]:
        return dict(delay=self.delay)

    def copy(self) -> GarbageLine:
        return GarbageLine(self.delay, self.index)


_Move = Literal[
    "move_left",
    "move_right",
    "rotate_cw",
    "rotate_ccw",
    "drop",
    "sonic_drop",
    "sonic_left",
    "sonic_right",
    "hold",
    "hard_drop",
]
_MOVES: tuple[_Move] = (
    "move_left",
    "move_right",
    "rotate_cw",
    "rotate_ccw",
    "drop",
    "sonic_drop",
    "sonic_left",
    "sonic_right",
    "hold",
    "hard_drop",
)


class Move:
    move_left: Move = None
    move_right: Move = None
    rotate_cw: Move = None
    rotate_ccw: Move = None
    drop: Move = None
    sonic_drop: Move = None
    sonic_left: Move = None
    sonic_right: Move = None
    hold: Move = None
    hard_drop: Move = None

    def __init__(self, val: str, idx: int):
        self.value: str = intern(val)
        self.index: int = idx

    @classmethod
    def from_str(cls, move_str: str) -> Move:
        return getattr(cls, move_str)

    @classmethod
    def from_index(cls, index: int) -> Move:
        return getattr(cls, _MOVES[index])

    @classmethod
    def from_command(cls, command: Command) -> Move:
        return getattr(cls, command)

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return self.index

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self.index < other.index


for index, value in enumerate(_MOVES):
    setattr(Move, value, Move(value, index))

MOVES: tuple[Move] = (
    Move.move_left,
    Move.move_right,
    Move.rotate_cw,
    Move.rotate_ccw,
    Move.drop,
    Move.sonic_drop,
    Move.sonic_left,
    Move.sonic_right,
    Move.hold,
    Move.hard_drop,
)


_Piece = Literal["I", "O", "J", "L", "S", "Z", "T"]
_PIECES: tuple[_Piece] = ("I", "O", "J", "L", "S", "Z", "T")


class Piece:

    I: Piece = None
    O: Piece = None
    J: Piece = None
    L: Piece = None
    S: Piece = None
    Z: Piece = None
    T: Piece = None

    def __init__(self, value: str, index: int):
        self.value: str = intern(value)
        self.index: int = index

    @classmethod
    def from_str(cls, value: str) -> Piece:
        return getattr(cls, value.upper())

    @classmethod
    def from_index(cls, index: int) -> Piece:
        return getattr(cls, _PIECES[index])

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return self.index

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self.index < other.index


for index, value in enumerate(_PIECES):
    setattr(Piece, value, Piece(value, index))

Block = Optional[Literal["I", "O", "J", "L", "S", "Z", "T", "G"]]
PIECES: tuple[Piece] = (Piece.I, Piece.O, Piece.J, Piece.L, Piece.S, Piece.Z, Piece.T)
Board = List[List[Block]]


@dataclass
class PieceData:
    piece: Piece = field(hash=True)
    x: int = field(hash=True)
    y: int = field(hash=True)
    rotation: Literal[0, 1, 2, 3] = field(hash=True)

    def copy(self) -> PieceData:
        return PieceData(self.piece, self.x, self.y, self.rotation)

    def __lt__(self, nxt):
        """
        Arbitrary comparison function to allow for heapq of PieceData objects
        """
        return (self.y, self.x, self.rotation) < (nxt.y, nxt.x, nxt.rotation)

    def __eq__(self, nxt):
        return (self.piece, self.y, self.x, self.rotation) == (
            nxt.piece,
            nxt.y,
            nxt.x,
            nxt.rotation,
        )

    def __hash__(self):
        return hash((self.piece.index, self.x, self.y, self.rotation))

    def public(self) -> dict[str, Piece | int]:
        return dict(piece=self.piece.value, x=self.x, y=self.y, rotation=self.rotation)


@dataclass
class AttackTable:
    single: int = 0
    double: int = 1
    triple: int = 2
    quad: int = 4
    ass: int = 2
    asd: int = 4
    ast: int = 6
    pc: int = 10
    b2b: int = 1

    def __post_init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def dict(self) -> dict[str, int]:
        return {
            "single": self.single,
            "double": self.double,
            "triple": self.triple,
            "quad": self.quad,
            "ass": self.ass,
            "asd": self.asd,
            "ast": self.ast,
            "pc": self.pc,
            "b2b": self.b2b,
        }


@dataclass
class Options:
    board_width: int = 10
    board_height: int = 20
    garbage_messiness: float = 0.05
    garbage_delay: int = 1
    attack_table: AttackTable = field(default_factory=AttackTable)
    combo_table: list[int] = field(
        default_factory=lambda: [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    )

    def __post_init__(self, **kwargs):
        if isinstance(self.attack_table, dict):
            self.attack_table = AttackTable(**self.attack_table)
        if not isinstance(self.attack_table, AttackTable):
            self.attack_table = AttackTable()

    def dict(self) -> dict[str, int | list[int] | dict[str, int]]:
        return {
            "board_width": self.board_width,
            "board_height": self.board_height,
            "garbage_messiness": self.garbage_messiness,
            "garbage_delay": self.garbage_delay,
            "attack_table": self.attack_table.dict(),
            "combo_table": self.combo_table,
        }


@dataclass
class ClearedLine:
    height: int
    blocks: list[Block]


@dataclass
class Event:
    type: str = field(init=False)

    @property
    def payload(self) -> dict[str, any]:
        attributes = asdict(self)
        return {key: value for key, value in attributes.items() if key != "type"}


@dataclass
class PiecePlacedEvent(Event):
    initial: PieceData
    final: PieceData

    def __post_init__(self):
        self.type = "piece_placed"


@dataclass
class DamageTankedEvent(Event):
    holeIndices: list[int]

    def __post_init__(self):
        self.type = "damage_tanked"


ClearName = Literal[
    "Single",
    "Triple",
    "Double",
    "Quad",
    "Perfect Clear",
    "All-Spin Single",
    "All-Spin Double",
    "All-Spin Triple",
]


@dataclass
class ClearEvent(Event):
    clearName: ClearName
    allSpin: bool
    b2b: bool
    combo: int
    pc: bool
    attack: int
    cancelled: int
    piece: PieceData
    clearedLines: list[ClearedLine]

    def __post_init__(self):
        self.type = "clear"


@dataclass
class GameOverEvent(Event):

    def __post_init__(self):
        self.type = "game_over"


@dataclass
class ScoreInfo:
    pc: bool
    lines_cleared: int
    is_immobile: bool
    b2b: bool
    combo: int


@dataclass
class ScoreData:
    score: int
    b2b: bool
    combo: int
    clear_name: ClearName | None
    all_spin: bool


@dataclass
class Statistics:
    heights: list[int]
    bumpiness: int
    avg_height: float
