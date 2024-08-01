from abc import ABC, abstractmethod
from game_state import GameState, Command

class BotInterface(ABC):
    @abstractmethod
    def get_next_move(self, game_state: GameState) -> Command:
        pass

    @abstractmethod
    def on_game_over(self, final_score: int):
        pass