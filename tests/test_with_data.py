import pickle
import unittest
from timeit import default_timer as timer
from typing import TYPE_CHECKING, Deque, List, Tuple

from botris import TetrisGame
from botris.engine import generate_moves
from botris.interface import Command, GameState


def cut_board(board: List[List[str]]) -> List[List[str]]:
    new_board = [
        ["G"] * 10 if any(cell == "G" for cell in row) else row for row in board
    ]
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


def verify_game_state(
    prev_game_state: GameState,
    game_state: GameState,
    prev_commands: List[Command],
    commands: List[Command],
) -> bool:
    gs = TetrisGame.from_game_state(prev_game_state)
    gs.execute_commands(prev_commands)
    predicted_gs = gs.get_public_state()
    if not check_gamestates(predicted_gs, game_state):
        print("Different game states")
        print(f"pred Gamestates: {predicted_gs} \n\n actualgs: {game_state}\n\n")
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


class TestGameState(unittest.TestCase):

    def test_buffer_gamestate(self):
        try:
            with open("test.game_buffer", "rb") as f:
                gb: GameBuffer = pickle.load(f)

            print(
                f"Analyzing gamestate engine. Games to Analyze: {gb.num_games}, frames to analyze: {gb.total_frames}"
            )
            for _, game in enumerate(gb.trajectory_buffer):
                for idx, val in enumerate(game):
                    if idx == 0:
                        continue
                    commands, game_state = val
                    prev_commands, prev_game_state = game[idx - 1]
                    if len(prev_commands) == 0 or prev_commands[-1] != "hard_drop":
                        prev_commands.append(Command("hard_drop"))
                    if not verify_game_state(
                        prev_game_state, game_state, prev_commands, commands
                    ):
                        print(
                            f"Found Error Game: {_}\nframe idx in game: {idx} \n\n prev gs: {prev_game_state} \n\n commands: {prev_commands} \n\n newgs: {game_state}"
                        )
                        self.fail("Game state verification failed")
        except FileNotFoundError:
            print("File not found, skipping...")

    def test_buffer_movegen(self):
        try:
            moves_found: int = 0
            cum_time: float = 0
            searches: int = 0

            move_lengths: int = 0

            with open("test.game_buffer", "rb") as f:
                gb: GameBuffer = pickle.load(f)

            print(
                f"Analyzing movegen. Games to Analyze: {gb.num_games}, frames to analyze: {gb.total_frames}"
            )
            for game in gb.trajectory_buffer:
                for trajectory in game:
                    prev_commands, prev_game_state = trajectory

                    gamestate = TetrisGame.from_game_state(prev_game_state)
                    start = timer()
                    moves = generate_moves(
                        gamestate.board,
                        gamestate.current.piece,
                        gamestate.held or gamestate.queue[0],
                        gamestate.options.board_height,
                        gamestate.options.board_width,
                        "bfs",
                    )
                    end = timer()
                    searches += 1

                    cum_time += end - start
                    moves_found += len(moves)
                    move_lengths += sum([len(move) for move in moves.values()])

                    for command in prev_commands:
                        if command == "hard_drop":
                            break
                        gamestate.execute_command(command)
                    gamestate.execute_command("sonic_drop")
                    if gamestate.current not in moves:
                        print(prev_game_state)
                        TetrisGame.from_game_state(prev_game_state).render_board()
                        gamestate.render_board()
                        print(prev_commands)
                        self.assertIn(gamestate.current, moves.keys())
                        print("HUH!")
                        self.fail("SOMETHING REALLY BAD HAPPENED")
            print(
                f"All Moves were found.\nTotal moves found: {moves_found}\nTotal time taken: {cum_time}\tAverage search time: {cum_time / searches}\nAverage moves per search: {moves_found / searches}\nAverage Move Length: {move_lengths / moves_found}"
            )
        except FileNotFoundError:
            print("File not found, skipping...")


if __name__ == "__main__":
    unittest.main()
