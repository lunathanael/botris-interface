from __future__ import annotations

import asyncio
from typing import Awaitable, Dict, List, Optional, Tuple

from botris.bots.bot import Bot
from botris.engine import TetrisGame
from botris.interface import Board, Command, GameState, PlayerData

from .src import AI, Snapshot, Statistics, Suggestion


def timeout_wrapper(func, timeout=1.0):
    async def wrapped_function(*args, **kwargs):
        try:
            return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
        except asyncio.TimeoutError:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                print(f"BlockFish Double Failure. Args: {args}, Kwargs: {kwargs}")
                args[0].shutdown()
                await args[0].start()
                return []
    return wrapped_function

class BlockFish(Bot):
    INPUT_MOVE_MAP: Dict[str, Command] ={
        'left': 'move_left',
        'right': 'move_right',
        'cw': 'rotate_cw',
        'ccw': 'rotate_ccw',
        'hold': 'hold',
        'sd': 'sonic_drop',
    }

    def __init__(self, node_limit: int=10000, timeout: Optional[float]=1):
        self.node_limit: int = node_limit
        self.timeout: Optional[float] = timeout
        if timeout is not None:
            self.analyze = timeout_wrapper(self.analyze, timeout=timeout)

    async def start(self) -> Awaitable[None]:
        self.ai: AI = AI()
        await self.ai.start()

    async def shutdown(self) -> Awaitable[None]:
        self.ai.shutdown()

    async def _analyze(self, snapshot) -> Awaitable[Tuple[List[Suggestion], Statistics]]:
        return await self.ai.analyze(snapshot, suggestion_limit=1, max_placements=1, node_limit=self.node_limit)

    async def analyze(self, game_state: GameState, players: List[PlayerData]) -> Awaitable[List[Command]]:
        gs: TetrisGame = TetrisGame.from_game_state(game_state)
        snapshot: Snapshot = BlockFish.to_snapshot(gs)
        res, stats = await self._analyze(snapshot)
        suggestion: Suggestion = res[0]
        rating: int = suggestion.rating
        moves: List[str] = suggestion.inputs
        moves: List[str] = format_moves(moves)
        commands: List[Command] = [
            Command(move)
            for move in moves
        ]
        return commands

    @staticmethod
    def to_snapshot(gs: TetrisGame) -> Snapshot:
        pgs: GameState = gs.get_public_state()
        queue: str = pgs.current.piece + ''.join(pgs.queue[:6])
        hold: Optional[str] = pgs.held
        matrix: Board = pgs.board
        matrix = [''.join(['x' if j else '.' for j in i]) for i in pgs.board]
        return Snapshot(queue, hold, matrix)


def format_moves(moves: List[str]) -> List[Command]:
    for i, move in enumerate(moves):
        if move == 'hd':
            return moves[:i]
        moves[i] = BlockFish.INPUT_MOVE_MAP[move]
