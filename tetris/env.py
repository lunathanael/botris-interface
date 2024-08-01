from game_state import GameState, Command, GameEvent
from typing import List, Tuple, Dict, Any
from utils import render_board

class TetrisEnv:
    def __init__(self, options: Dict[str, Any] = None):
        self.options = self.get_default_options()
        if options:
            self.options.update(options)
        self.game_state = GameState.create_game_state(self.options)

    @staticmethod
    def get_default_options() -> Dict[str, Any]:
        return {
            "board_width": 10,
            "board_height": 20,
            "garbage_messiness": 0.05,
            "attack_table": {
                "single": 0,
                "double": 1,
                "triple": 2,
                "quad": 4,
                "asd": 4,
                "ass": 2,
                "ast": 6,
                "pc": 10,
                "b2b": 1,
            },
            "combo_table": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
        }

    def reset(self) -> GameState:
        self.game_state = GameState.create_game_state(self.options)
        return self.game_state

    def step(self, command: Command) -> Tuple[GameState, List[GameEvent]]:
        new_game_state, events = self.game_state.execute_command(command, self.options)
        self.game_state = new_game_state
        return new_game_state, events

    def get_public_game_state(self) -> Dict[str, Any]:
        return self.game_state.get_public_game_state()

    def render(self):
        render_board(self.game_state.board)