from typing import Awaitable, List

from botris.interface import Command, GameState, PlayerData


class Bot:
    def __init__(self, *args, **kwargs):
        pass

    async def analyze(
        self, game_state: GameState, players: List[PlayerData]
    ) -> Awaitable[List[Command]]:
        raise NotImplementedError("Analyze method must be implemented for bot")

    async def start(self) -> Awaitable[None]:
        return None

    def shutdown(self) -> None:
        return None

    def __del__(self):
        self.shutdown()
