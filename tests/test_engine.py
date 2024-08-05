import pickle
import unittest
from timeit import default_timer as timer
from typing import TYPE_CHECKING, Deque, List, Tuple

from botris import TetrisGame
from botris.engine import Event, Piece, generate_garbage
from botris.interface import PublicGarbageLine


class TestTetrisGame(unittest.TestCase):

    def test_sonic_drop(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("sonic_drop")
        self.assertEqual(game.current.y, 1)

    def test_move_horizontally(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        self.assertEqual(game.current.x, 3)
        game.execute_command("move_right")
        self.assertEqual(game.current.x, 4)
        game.execute_command("sonic_left")
        self.assertEqual(game.current.x, 0)
        game.execute_command("move_left")
        self.assertEqual(game.current.x, 0)

    def test_hard_drop(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("hard_drop")
        expected_board = [[None] * 3 + ["I"] * 4 + [None] * 3]
        self.assertEqual(game.board, expected_board)

    def test_tspin(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 10,
            [None] * 3 + ["G"] + [None] * 2 + ["G"] + [None] * 3,
            ["G"] * 3 + [None] * 3 + ["G"] * 4,
            ["G"] * 4 + [None] + ["G"] * 5,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.T)
        game.current = game.next_piece()
        game.execute_command("rotate_cw")
        game.execute_command("sonic_drop")
        game.execute_command("rotate_cw")
        result = game.execute_command("hard_drop")
        self.assertTrue(any([event.type == "clear" for event in result]))
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["attack"], 4)
        self.assertEqual(clear_event.payload["clearName"], "All-Spin Double")

    def test_oclear(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 4 + ["G"] * 2 + [None] * 4,
            ["G"] * 4 + [None] * 2 + ["G"] * 4,
            ["G"] * 4 + [None] * 2 + ["G"] * 4,
            [None] * 4 + ["G"] * 2 + [None] * 4,
            *[[None] * 10 for _ in range(18)],
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.O)
        game.current = game.next_piece()
        result = game.execute_command("hard_drop")
        self.assertTrue(any([event.type == "clear" for event in result]))
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["attack"], 1)
        self.assertEqual(clear_event.payload["clearName"], "Double")

    def test_ospin(self):
        game = TetrisGame()
        tspin_setup = [
            [None] * 4 + ["G"] * 2 + [None] * 4,
            ["G"] * 4 + [None] * 2 + ["G"] * 4,
            ["G"] * 4 + [None] * 2 + ["G"] * 4,
            [None] * 4 + ["G"] * 2 + [None] * 4,
            *[[None] * 10 for _ in range(18)],
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        game.queue.appendleft(Piece.O)
        game.current = game.next_piece()
        game.execute_command("rotate_cw")
        result = game.execute_command("hard_drop")
        self.assertTrue(any([event.type == "clear" for event in result]))
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["attack"], 4)
        self.assertEqual(clear_event.payload["clearName"], "All-Spin Double")

    def test_tspin_wallkick(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.next_piece()
        tspin_setup = [
            [None] * 10,
            [None] * 3 + ["G"] + [None] * 2 + ["G"] + [None] * 3,
            ["G"] * 3 + [None] * 3 + ["G"] * 4,
            ["G"] * 4 + [None] + ["G"] * 5,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command("move_right")
        game.execute_command("rotate_ccw")
        game.execute_command("sonic_drop")
        game.execute_command("rotate_ccw")
        result = game.execute_command("hard_drop")

        self.assertTrue(any([event.type == "clear" for event in result]))
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["attack"], 4)
        self.assertEqual(clear_event.payload["clearName"], "All-Spin Double")

    def test_add_garbage(self):
        game = TetrisGame()
        public_garbage_lines = [PublicGarbageLine(delay=dly) for dly in [0, 0, 1, 2]]
        garbage_lines = generate_garbage(
            public_garbage_lines,
            game.options.garbage_messiness,
            game.options.board_width,
        )
        game.queue_garbage_lines(garbage_lines)
        self.assertFalse(any("G" in row for row in game.board))
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("hard_drop")
        self.assertTrue("G" in game.board[0])
        self.assertTrue("G" in game.board[1])
        self.assertFalse(len(game.board) >= 3 and "G" in game.board[2])
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("hard_drop")
        self.assertTrue("G" in game.board[0])
        self.assertTrue("G" in game.board[1])
        self.assertTrue("G" in game.board[2])
        self.assertFalse(len(game.board) >= 4 and "G" in game.board[3])
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("hard_drop")
        self.assertTrue("G" in game.board[0])
        self.assertTrue("G" in game.board[1])
        self.assertTrue("G" in game.board[2])
        self.assertTrue("G" in game.board[3])

    def test_single_clear(self):
        game = TetrisGame()
        single_clear_setup = [
            ["I"] + [None] * 9,
            ["I", "I", "I", "I", "I", "I", None, None, None, None],
        ]
        single_clear_setup.reverse()
        game.board = single_clear_setup

        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("sonic_right")
        result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "Single")

    def test_double_clear(self):
        game = TetrisGame()
        double_clear_setup = [
            ["I"] + [None] * 9,
            ["I", "I", "I", "I", "I", "I", "I", "I", None, None],
            ["I", "I", "I", "I", "I", "I", "I", "I", None, None],
        ]
        double_clear_setup.reverse()
        game.board = double_clear_setup

        game.queue.appendleft(Piece.O)
        game.current = game.next_piece()
        game.execute_command("sonic_right")
        result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "Double")

    def test_triple_clear(self):
        game = TetrisGame()
        triple_clear_setup = [
            [None] * 10,
            [None] * 10,
            [None] * 10,
            [None] * 10,
            ["I"] + [None] * 9,
            ["I", "I", "I", "I", "I", "I", "I", "I", None, None],
            ["I", "I", "I", "I", "I", "I", "I", "I", "I", None],
            ["I", "I", "I", "I", "I", "I", "I", "I", "I", None],
        ]
        triple_clear_setup.reverse()
        game.board = triple_clear_setup

        game.queue.appendleft(Piece.L)
        game.current = game.next_piece()
        game.execute_command("rotate_ccw")
        game.execute_command("sonic_right")
        result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "Triple")

    def test_quad_clear(self):
        game = TetrisGame()
        result: List[Event] = []

        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("rotate_ccw")
        game.execute_command("sonic_left")
        result = game.execute_command("hard_drop")
        for i in range(10):
            game.queue.appendleft(Piece.I)
            game.current = game.next_piece()
            game.execute_command("rotate_ccw")
            game.execute_command("sonic_left")
            for j in range(i):
                game.execute_command("move_right")
            result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "Quad")

    def test_perfect_clear(self):
        game = TetrisGame()
        perfect_clear_setup = [
            [None] * 10,
            [None] * 10,
            [None] * 10,
            [None] * 10,
            ["I", "I", "I", "I", "I", None, "I", "I", "I", "I", "I"],
            ["I", "I", "I", "I", "I", None, "I", "I", "I", "I", "I"],
            ["I", "I", "I", "I", "I", None, "I", "I", "I", "I", "I"],
            ["I", "I", "I", "I", "I", None, "I", "I", "I", "I", "I"],
        ]
        perfect_clear_setup.reverse()
        game.board = perfect_clear_setup
        game.queue.appendleft(Piece.I)
        game.current = game.next_piece()
        game.execute_command("rotate_ccw")
        game.execute_command("move_right")
        result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "Perfect Clear")

    def test_all_spin_single_clear(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.next_piece()
        tspin_setup = [
            [None] * 10,
            ["G"] * 8 + [None] * 2,
            ["G"] * 8 + [None] * 2,
            ["G"] * 7 + [None] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command("rotate_ccw")
        game.execute_command("sonic_right")
        game.execute_command("sonic_drop")
        game.execute_command("rotate_cw")
        result = game.execute_command("hard_drop")
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "All-Spin Single")

    def test_all_spin_triple_clear(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.next_piece()
        tspin_setup = [
            [None] * 6 + ["G"] * 4,
            [None] * 7 + ["G"] * 3,
            ["G"] * 6 + [None] + ["G"] * 3,
            ["G"] * 5 + [None] * 2 + ["G"] * 3,
            ["G"] * 6 + [None] + ["G"] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command("sonic_drop")
        game.execute_command("sonic_right")
        game.execute_command("rotate_ccw")
        result = game.execute_command("hard_drop")
        self.assertTrue(any([event.type == "clear" for event in result]))
        clear_event = next((event for event in result if event.type == "clear"), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event.payload["clearName"], "All-Spin Triple")


if __name__ == "__main__":
    unittest.main()
