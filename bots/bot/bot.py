from typing import List

from interface.models import Command, GameState, PlayerData


class Bot:
    def __init__(self, *args, **kwargs):
        pass

    async def analyze(self, game_state: GameState, players: List[PlayerData]) -> List[Command]:
        raise NotImplementedError("Subclasses must implement this method")

    async def start(self):
        raise NotImplementedError("Subclasses must implement this method")

    def shutdown(self):
        raise NotImplementedError("Subclasses must implement this method")

    def __del__(self):
        self.shutdown()