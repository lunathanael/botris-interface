from typing import List

from engine.tetris import TetrisGame

from .models import Command, GameState, PlayerData


def process_game_state(game_state: GameState, players: List[PlayerData]) -> List[Command]:
    commands = [
        Command(command="move_left"),
        Command(command="rotate_cw"),
        Command(command="drop")
    ]
    gs = TetrisGame.from_game_state(game_state)
    gs.render_board()
    return commands
