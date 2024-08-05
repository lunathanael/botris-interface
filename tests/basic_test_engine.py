import unittest

from botris import TetrisGame
from botris.engine import Move, PieceData
from botris.interface import PublicGarbageLine


class TestTetrisGame(unittest.TestCase):

    def test_spawn_piece(self):
        game = TetrisGame()
        piece = game.next_piece()
        self.assertIsInstance(piece, PieceData)

    def test_queue_garbage(self):
        game = TetrisGame()
        game.queue_garbage([0, 1, 2])
        self.assertEqual(len(game.garbage_queue), 3)

    def test_queue_garbage_lines(self):
        game = TetrisGame()
        garbage_lines = [PublicGarbageLine(delay=0), PublicGarbageLine(delay=1)]
        game.queue_garbage_lines(garbage_lines)
        self.assertEqual(len(game.garbage_queue), 2)

    def test_execute_command(self):
        game = TetrisGame()
        events = game.execute_command("move_left")
        self.assertIsInstance(events, list)

    def test_execute_commands(self):
        game = TetrisGame()
        commands = ["move_left", "move_right"]
        events = game.execute_commands(commands)
        self.assertIsInstance(events, list)

    def test_execute_moves(self):
        game = TetrisGame()
        moves = [Move.move_left, Move.move_right]
        events = game.execute_moves(moves)
        self.assertIsInstance(events, list)

    def test_get_board_stats(self):
        game = TetrisGame()
        stats = game.get_board_stats()
        self.assertIsNotNone(stats)

    def test_generate_moves(self):
        game = TetrisGame()
        moves = game.generate_moves()
        self.assertIsInstance(moves, dict)


if __name__ == "__main__":
    unittest.main()
