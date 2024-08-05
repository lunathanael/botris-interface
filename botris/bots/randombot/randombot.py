from __future__ import annotations

import random
from typing import Awaitable, Dict, List

from botris.bots.bot import Bot
from botris.engine import Move, PieceData, TetrisGame
from botris.interface import Command, GameState, PlayerData


class RandomBot(Bot):

    def __init__(self):
        return

    async def start(self) -> Awaitable[None]:
        return

    def shutdown(self) -> None:
        return

    async def analyze(self, game_state: GameState, players: List[PlayerData]) -> Awaitable[List[Command]]:
        gs: TetrisGame = TetrisGame.from_game_state(game_state)
        moves: Dict[PieceData, List[Move]] = gs.generate_moves()
        if not moves:
            return []

        move: List[Move] = random.choice(list(moves.values()))
        move: List[Command] = [Command.from_move(m) for m in move]
        return move
