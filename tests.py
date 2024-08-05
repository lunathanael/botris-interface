import pickle
import unittest
from typing import TYPE_CHECKING, List, Tuple

from engine import TetrisGame
from engine.utils import generate_garbage
from interface.models import Command, GameState
from engine.move_generator import generate_moves
from engine.pieces import Piece
from timeit import default_timer as timer

if TYPE_CHECKING:
    from engine.models import Event


class TestTetrisGame(unittest.TestCase):

    def test_sonic_drop(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        game.execute_command('sonic_drop')
        self.assertEqual(game.current.y, 1)

    def test_move_horizontally(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        self.assertEqual(game.current.x, 3)
        game.execute_command('move_right')
        self.assertEqual(game.current.x, 4)
        game.execute_command('sonic_left')
        self.assertEqual(game.current.x, 0)
        game.execute_command('move_left')
        self.assertEqual(game.current.x, 0)

    def test_hard_drop(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        game.execute_command('hard_drop')
        expected_board = [[None] * 3 + ['I'] * 4 + [None] * 3]
        self.assertEqual(game.board, expected_board)

    def test_tspin(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 10,
            [None] * 3 + ['G'] + [None] * 2 + ['G'] + [None] * 3,
            ['G'] * 3 + [None] * 3 + ['G'] * 4,
            ['G'] * 4 + [None] + ['G'] * 5,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        game.execute_command('rotate_cw')
        game.execute_command('sonic_drop')
        game.execute_command('rotate_cw')
        result = game.execute_command('hard_drop')
        self.assertTrue(any([event.type == 'clear' for event in result]))
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['attack'], 4)
        self.assertEqual(clear_event.payload['clearName'], 'All-Spin Double')

    def test_oclear(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 4 + ['G'] * 2 + [None] * 4,
            ['G'] * 4 + [None] * 2 + ['G'] * 4,
            ['G'] * 4 + [None] * 2 + ['G'] * 4,
            [None] * 4 + ['G'] * 2 + [None] * 4,
            *[
                [None] * 10
                for _ in range(18)
            ]
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.O)
        game.current = game.spawn_piece()
        result = game.execute_command('hard_drop')
        self.assertTrue(any([event.type == 'clear' for event in result]))
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['attack'], 1)
        self.assertEqual(clear_event.payload['clearName'], 'Double')

    def test_ospin(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 4 + ['G'] * 2 + [None] * 4,
            ['G'] * 4 + [None] * 2 + ['G'] * 4,
            ['G'] * 4 + [None] * 2 + ['G'] * 4,
            [None] * 4 + ['G'] * 2 + [None] * 4,
            *[
                [None] * 10
                for _ in range(18)
            ]
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.O)
        game.current = game.spawn_piece()
        game.execute_command('rotate_cw')
        result = game.execute_command('hard_drop')
        self.assertTrue(any([event.type == 'clear' for event in result]))
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['attack'], 4)
        self.assertEqual(clear_event.payload['clearName'], 'All-Spin Double')

    def test_tspin_wallkick(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 10,
            [None] * 3 + ['G'] + [None] * 2 + ['G'] + [None] * 3,
            ['G'] * 3 + [None] * 3 + ['G'] * 4,
            ['G'] * 4 + [None] + ['G'] * 5,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command('move_right')
        game.execute_command('rotate_ccw')
        game.execute_command('sonic_drop')
        game.execute_command('rotate_ccw')
        result = game.execute_command('hard_drop')

        self.assertTrue(any([event.type == 'clear' for event in result]))
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['attack'], 4)
        self.assertEqual(clear_event.payload['clearName'], 'All-Spin Double')

    def test_add_garbage(self):
        game = TetrisGame()
        garbage_indices = generate_garbage(4, game.options.garbage_messiness, game.options.board_width)
        game.queue_garbage(garbage_indices)
        self.assertFalse(any('G' in row for row in game.board))
        game.execute_command('hard_drop')
        self.assertTrue('G' in game.board[0])
        self.assertTrue('G' in game.board[3])

    def test_single_clear(self):
        game = TetrisGame()
        single_clear_setup = [
            ['I'] + [None] * 9,
            ['I', 'I', 'I', 'I', 'I', 'I', None, None, None, None],
        ]
        single_clear_setup.reverse()
        game.board = single_clear_setup

        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        game.execute_command('sonic_right')
        result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'Single')

    def test_double_clear(self):
        game = TetrisGame()
        double_clear_setup = [
            ['I'] + [None] * 9,
            ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', None, None],
            ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', None, None],
        ]
        double_clear_setup.reverse()
        game.board = double_clear_setup

        game.queue.appendleft(Piece.O)
        game.current = game.spawn_piece()
        game.execute_command('sonic_right')
        result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'Double')

    def test_triple_clear(self):
        game = TetrisGame()
        triple_clear_setup = [
            [None] * 10,
            [None] * 10,
            [None] * 10,
            [None] * 10,
            ['I'] + [None] * 9,
            ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', None, None],
            ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', None],
            ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', None],
        ]
        triple_clear_setup.reverse()
        game.board = triple_clear_setup

        game.queue.appendleft(Piece.L)
        game.current = game.spawn_piece()
        game.execute_command('rotate_ccw')
        game.execute_command('sonic_right')
        result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'Triple')

    def test_quad_clear(self):
        game = TetrisGame()
        result: List[Event] = []
        
        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        game.execute_command('rotate_ccw')
        game.execute_command('sonic_left')
        result = game.execute_command('hard_drop')
        for i in range(10):
            game.queue.appendleft(Piece.I)
            game.current = game.spawn_piece()
            game.execute_command('rotate_ccw')
            game.execute_command('sonic_left')
            for j in range(i):
                game.execute_command('move_right')
            result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'Quad')

    def test_perfect_clear(self):
        game = TetrisGame()
        perfect_clear_setup = [
            [None] * 10,
            [None] * 10,
            [None] * 10,
            [None] * 10,
            ['I', 'I', 'I', 'I', 'I', None, 'I', 'I', 'I', 'I', 'I'],
            ['I', 'I', 'I', 'I', 'I', None, 'I', 'I', 'I', 'I', 'I'],
            ['I', 'I', 'I', 'I', 'I', None, 'I', 'I', 'I', 'I', 'I'],
            ['I', 'I', 'I', 'I', 'I', None, 'I', 'I', 'I', 'I', 'I'],
        ]
        perfect_clear_setup.reverse()
        game.board = perfect_clear_setup
        game.queue.appendleft(Piece.I)
        game.current = game.spawn_piece()
        game.execute_command('rotate_ccw')
        game.execute_command('move_right')
        result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'Perfect Clear')

    def test_all_spin_single_clear(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 10,
            ['G'] * 8 + [None] * 2,
            ['G'] * 8 + [None] * 2,
            ['G'] * 7 + [None] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command('rotate_ccw')
        game.execute_command('sonic_right')
        game.execute_command('sonic_drop')
        game.execute_command('rotate_cw')
        result = game.execute_command('hard_drop')
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'All-Spin Single')

    def test_all_spin_triple_clear(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 6 + ['G'] * 4,
            [None] * 7 + ['G'] * 3,
            ['G'] * 6 + [None] + ['G'] * 3,
            ['G'] * 5 + [None] * 2 + ['G'] * 3,
            ['G'] * 6 + [None] + ['G'] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command('sonic_drop')
        game.execute_command('sonic_right')
        game.execute_command('rotate_ccw')
        result = game.execute_command('hard_drop')
        self.assertTrue(any([event.type == 'clear' for event in result]))
        clear_event = next((event for event in result if event.type == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload['clearName'], 'All-Spin Triple')

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
    gs.execute_commands(prev_commands)
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

class TestGameState(unittest.TestCase):

    def test_buffer_gamestate(self):
        try:
            with open('test.game_buffer', 'rb') as f:
                gb: GameBuffer = pickle.load(f)

            print(f'Analyzing gamestate engine. Games to Analyze: {gb.num_games}, frames to analyze: {gb.total_frames}')
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
                        self.fail("Game state verification failed")
        except FileNotFoundError:
            print("File not found")
            self.fail("File not found")

    def test_buffer_movegen(self):
        try:
            moves_found: int = 0
            cum_time: float = 0
            searches: int = 0

            move_lengths: int = 0

            with open('test.game_buffer', 'rb') as f:
                gb: GameBuffer = pickle.load(f)

            print(f'Analyzing movegen. Games to Analyze: {gb.num_games}, frames to analyze: {gb.total_frames}')
            for game in gb.trajectory_buffer:
                for trajectory in game:
                    prev_commands, prev_game_state = trajectory

                    gamestate = TetrisGame.from_game_state(prev_game_state)
                    start = timer()
                    moves = generate_moves(gamestate.board, gamestate.current.piece, gamestate.held or gamestate.queue[0], gamestate.options.board_height, gamestate.options.board_width, 'bfs')
                    end = timer()
                    searches += 1

                    cum_time += end - start
                    moves_found += len(moves)
                    move_lengths += sum([len(move) for move in moves.values()])

                    for command in prev_commands:
                        if command == 'hard_drop':
                            break
                        gamestate.execute_command(command)
                    gamestate.execute_command('sonic_drop')
                    if gamestate.current not in moves:
                        print(prev_game_state)
                        TetrisGame.from_game_state(prev_game_state).render_board()
                        gamestate.render_board()
                        print(prev_commands)
                        self.assertIn(gamestate.current, moves.keys())
                        print("HUH!")
                        self.fail("SOMETHING REALLY BAD HAPPENED")
            print(f"All Moves were found.\nTotal moves found: {moves_found}\nTotal time taken: {cum_time}\tAverage search time: {cum_time / searches}\nAverage moves per search: {moves_found / searches}\nAverage Move Length: {move_lengths / moves_found}")
        except FileNotFoundError:
            print("File not found")
            self.fail("File not found")

class TestMoveGenerator(unittest.TestCase):

    def test_tspin(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 10,
            ['G'] * 8 + [None] * 2,
            ['G'] * 8 + [None] * 2,
            ['G'] * 7 + [None] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        moves = generate_moves(game.board, game.current.piece, game.held, game.options.board_height, game.options.board_width)

        game.execute_command('rotate_ccw')
        game.execute_command('sonic_right')
        game.execute_command('sonic_drop')
        game.execute_command('rotate_cw')
        game.execute_command('sonic_drop')
        current_piece = game.current
        self.assertIn(current_piece, moves.keys())

if __name__ == '__main__':
    unittest.main()