from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional, Tuple

from pydantic import BaseModel, constr

if TYPE_CHECKING:
    from botris.engine.models import Move

Piece = Literal["I", "O", "J", "L", "S", "Z", "T"]
Block = Optional[Literal["I", "O", "J", "L", "S", "Z", "T", "G"]]
Board = List[List[Block]]

SessionId = str


class PlayerInfo(BaseModel):
    userId: str
    creator: str
    bot: str


class PlayerData(BaseModel):
    sessionId: str
    playing: bool
    info: PlayerInfo
    wins: int
    gameState: GameState | None


class RoomData(BaseModel):
    id: str
    host: PlayerInfo
    private: bool
    ft: int
    initialPps: float
    finalPps: int
    startMargin: int
    endMargin: int
    maxPlayers: int
    gameOngoing: bool
    roundOngoing: bool
    startedAt: int | None
    endedAt: int | None
    lastWinner: str | None
    players: list[PlayerData]
    banned: list[PlayerInfo]


class PieceData(BaseModel):
    piece: Piece
    x: int
    y: int
    rotation: Literal[0, 1, 2, 3]


class PublicGarbageLine(BaseModel):
    delay: int


class GameState(BaseModel):
    board: Board
    queue: list[Piece]
    garbageQueued: list[PublicGarbageLine]
    held: Piece | None
    current: PieceData
    canHold: bool
    combo: int
    b2b: bool
    score: int
    piecesPlaced: int
    garbageCleared: int
    dead: bool


class Command(str):
    hold: Command = None
    move_left: Command = None
    move_right: Command = None
    sonic_left: Command = None
    sonic_right: Command = None
    rotate_cw: Command = None
    rotate_ccw: Command = None
    drop: Command = None
    sonic_drop: Command = None
    hard_drop: Command = None

    def __init__(self, command: str):
        super().__init__()

    @classmethod
    def from_move(cls, move: Move) -> Command:
        return cls(move.value)


COMMANDS: tuple[Command] = (
    "hold",
    "move_left",
    "move_right",
    "sonic_left",
    "sonic_right",
    "rotate_cw",
    "rotate_ccw",
    "drop",
    "sonic_drop",
    "hard_drop",
)


for value in COMMANDS:
    setattr(Command, value, Command(value))
