import unittest
from timeit import default_timer as timer
from typing import TYPE_CHECKING, Deque, List, Tuple

from botris import TetrisGame
from botris.engine import Piece, generate_moves


class TestMoveGenerator(unittest.TestCase):

    def test_tspin(self):
        game = TetrisGame()
        game.queue.appendleft(Piece.T)
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 10,
            ["G"] * 8 + [None] * 2,
            ["G"] * 8 + [None] * 2,
            ["G"] * 7 + [None] * 3,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup

        moves = generate_moves(
            game.board,
            game.current.piece,
            game.held,
            game.options.board_height,
            game.options.board_width,
        )

        game.execute_command("rotate_ccw")
        game.execute_command("sonic_right")
        game.execute_command("sonic_drop")
        game.execute_command("rotate_cw")
        game.execute_command("sonic_drop")
        current_piece = game.current
        self.assertIn(current_piece, moves.keys())


if __name__ == "__main__":
    unittest.main()
