from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, constr

Piece = Literal['I', 'O', 'J', 'L', 'S', 'Z', 'T']
Block = Optional[Literal['I', 'O', 'J', 'L', 'S', 'Z', 'T', 'G']]
Board = List[List[Block]]

class PlayerInfo(BaseModel):
    userId: str
    creator: str
    bot: str

class PlayerData(BaseModel):
    sessionId: str
    playing: bool
    info: PlayerInfo
    wins: int
    gameState: Optional[GameState]

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
    startedAt: Optional[int]
    endedAt: Optional[int]
    lastWinner: Optional[str]
    players: List[PlayerData]
    banned: List[PlayerInfo]

class PieceData(BaseModel):
    piece: Piece
    x: int
    y: int
    rotation: Literal[0, 1, 2, 3]

class GameState(BaseModel):
    board: Board
    queue: List[Piece]
    garbageQueued: int
    held: Optional[Piece]
    current: PieceData
    canHold: bool
    combo: int
    b2b: bool
    score: int
    piecesPlaced: int
    dead: bool

class Command(str):
    def __new__(cls, command: str):
        return str.__new__(cls, command)

    def __init__(self, command: str):
        super().__init__()