from interface.models import GameState, Command
from engine import TetrisGame
from typing import List, Tuple
import asyncio
import pickle

def cut_board(board: List[List[str]]) -> List[List[str]]:
    new_board = [row for row in board if any(cell != 'G' and cell is not None for cell in row)]
    return new_board

def check_gamestates(gs1: GameState, gs2: GameState) -> bool:
    b1 = cut_board(gs1.board)
    b2 = cut_board(gs2.board)
    if b1 != b2:
        print("Different board")
        gs1.board = b1
        gs2.board = b2
        return False
    if gs1.queue[:4] != gs2.queue[:4]:
        print("Different queue")
        return False
    if gs1.held != gs2.held:
        print("Different held")
        return False
    if gs1.current != gs2.current:
        print("Different current")
        return False
    if gs1.isImmobile:
        print("Different isImmobile")
        return False
    if gs1.canHold != gs2.canHold:
        print("Different canHold")
        return False
    if gs1.combo != gs2.combo:
        print("Different combo")
        return False
    if gs1.b2b != gs2.b2b:
        print("Different b2b")
        return False
    if gs1.score != gs2.score:
        print("Different score")
        return False
    if gs1.piecesPlaced != gs2.piecesPlaced:
        print("Different piecesPlaced")
        return False
    if gs1.dead != gs2.dead:
        print("Different dead")
        return False
    return True

def verify_game_state(prev_game_state: GameState, game_state: GameState, prev_commands: List[Command], commands: List[Command]) -> bool:
    gs = TetrisGame.from_game_state(prev_game_state)
    for command in prev_commands:
        gs.execute_command(command)
    predicted_gs = gs.get_public_state()
    if not check_gamestates(predicted_gs, game_state):
        print("Different game states")
        print(f'pred Gamestates: {predicted_gs} \n\n actualgs: {game_state}\n\n')
        return False
    return True

class GameBuffer:
    def __init__(self):
        self.num_games: int = 0
        self.total_frames: int = 0
        self.trajectory_buffer: List[List[Tuple[List[Command], GameState]]] = []

    def add_frame(self, game_state: GameState, commands: List[Command]):
        if self.num_games == 0:
            self.trajectory_buffer.append([])
        self.trajectory_buffer[-1].append((commands, game_state))
        self.total_frames += 1

    def new_game(self):
        self.num_games += 1
        self.trajectory_buffer.append([])

async def main():
    with open('test.game_buffer', 'rb') as f:
        gb: GameBuffer = pickle.load(f)

    print(f'Games to Analyze: {gb.num_games}, frames to analyze: {gb.total_frames}')
    for _, game in enumerate(gb.trajectory_buffer):
        for idx, val in enumerate(game):
            if idx == 0:
                continue
            commands, game_state = val
            prev_commands, prev_game_state = game[idx - 1]
            if len(prev_commands) == 0 or prev_commands[-1] != 'hard_drop':
                prev_commands.append(Command('hard_drop'))

            if not verify_game_state(prev_game_state, game_state, prev_commands, commands):

                print(f'Found Error Game: {_}\nframe idx in game: {idx} \n\n prev gs: {prev_game_state} \n\n commands: {prev_commands} \n\n newgs: {game_state}')

if __name__ == "__main__":
    asyncio.run(main())