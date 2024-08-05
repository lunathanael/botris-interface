from typing import Awaitable, List

from botris.interface import Command, GameState, PlayerData


class Bot:
    def __init__(self, *args, **kwargs):
        pass

    async def analyze(self, game_state: GameState, players: List[PlayerData]) -> Awaitable[List[Command]]:
        raise NotImplementedError("Subclasses must implement this method")

    async def start(self) -> Awaitable[None]:
        raise NotImplementedError("Subclasses must implement this method")

    def shutdown(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    def __del__(self):
        self.shutdown()