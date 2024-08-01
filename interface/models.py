from typing import List, Optional, Union
from pydantic import BaseModel, constr

class PlayerInfo(BaseModel):
    userId: str
    creator: str
    bot: str

class PlayerData(BaseModel):
    sessionId: str
    playing: bool
    info: PlayerInfo
    wins: int
    gameState: Optional['GameState']

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
    piece: str
    x: int
    y: int
    rotation: int

class GameState(BaseModel):
    board: List[List[Union[str, None]]]
    queue: List[str]
    garbageQueued: int
    held: Optional[str]
    current: PieceData
    isImmobile: bool
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