from __future__ import annotations

import random
from typing import Dict, List

from botris.bots.bot import Bot
from botris.engine import Command, GameAction, PieceData, TetrisGame
from botris.interface import Command, GameState, PlayerData


class RandomBot(Bot):

    def __init__(self):
        return

    async def start(self):
        return

    def shutdown(self):
        return

    async def analyze(self, game_state: GameState, players: List[PlayerData]) -> List[Command]:
        gs: TetrisGame = TetrisGame.from_game_state(game_state)
        moves: Dict[PieceData, GameAction] = gs.generate_moves()
        if not moves:
            return []

        move: GameAction = random.choice(list(moves.values()))
        return move
