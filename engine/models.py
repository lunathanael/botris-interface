from __future__ import annotations
from typing import List, Optional, Tuple, Literal, Dict
from dataclasses import dataclass, field, asdict
import copy


Piece = Literal['I', 'O', 'J', 'L', 'S', 'Z', 'T']
Block = Optional[Literal['I', 'O', 'J', 'L', 'S', 'Z', 'T', 'G']]

PIECES: Tuple[Piece] = ('I', 'O', 'J', 'L', 'S', 'Z', 'T')

Board = List[List[Block]]

@dataclass
class PieceData:
    piece: Piece
    x: int
    y: int
    rotation: Literal[0, 1, 2, 3]

    def copy(self) -> PieceData:
        return PieceData(self.piece, self.x, self.y, self.rotation)

@dataclass
class AttackTable:
    single: int = 0
    double: int = 1
    triple: int = 2
    quad: int = 4
    asd: int = 4
    ass: int = 2
    ast: int = 6
    pc: int = 10
    b2b: int = 1

    def __post_init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass
class Options:
    board_width: int = 10
    board_height: int = 20
    garbage_messiness: float = 0.05
    attack_table: AttackTable = field(default_factory=AttackTable)
    combo_table: List[int] = field(default_factory=lambda: [0, 0, 1, 1, 1, 2, 2, 3, 3, 4])

    def __post_init__(self, **kwargs):
        if isinstance(self.attack_table, dict):
            self.attack_table = AttackTable(**self.attack_table)
        if not isinstance(self.attack_table, AttackTable):
            self.attack_table = AttackTable()

Command = Literal['hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_ccw', 'drop', 'sonic_drop']

@dataclass
class ClearedLine:
    height: int
    blocks: List[Block]

@dataclass
class Event:
    type: str = field(init=False)

    @property
    def payload(self) -> Dict[str, any]:
        attributes = asdict(self)
        return {key: value for key, value in attributes.items() if key != 'type'}

@dataclass
class PiecePlacedEvent(Event):
    initial: PieceData
    final: PieceData

    def __post_init__(self):
        self.type = 'piece_placed'

@dataclass
class DamageTankedEvent(Event):
    holeIndices: List[int]

    def __post_init__(self):
        self.type = 'damage_tanked'

ClearName = Literal['Single', 'Triple', 'Double', 'Quad', 'Perfect Clear', 'All-Spin Single', 'All-Spin Double', 'All-Spin Triple']

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
    clearedLines: List[ClearedLine]

    def __post_init__(self):
        self.type = 'clear'

@dataclass
class GameOverEvent(Event):

    def __post_init__(self):
        self.type = 'game_over'

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
    clear_name: Optional[ClearName]
    all_spin: bool

@dataclass
class Statistics:
    heights: List[int]
    bumpiness: int
    avg_height: float