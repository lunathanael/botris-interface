from interface.models import GameState, PlayerData, Command
from typing import List

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