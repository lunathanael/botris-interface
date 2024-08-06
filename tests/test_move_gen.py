import random
import unittest
from timeit import default_timer as timer
from typing import TYPE_CHECKING, Deque, List, Tuple

from botris import TetrisGame
from botris.engine import Piece, generate_moves


class TestMoveGenerator(unittest.TestCase):

    def test_tspin(self):
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

    def test_200_moves(self):
        game = TetrisGame()
        games: int = 0
        for _ in range(200):
            moves = game.generate_moves()
            if game.dead:
                self.assertFalse(moves)
                games += 1
                game.reset()
                moves = game.generate_moves()
            self.assertTrue(len(moves) > 0)
            d1: bool = None
            d2: bool = None
            for piece_data, move in moves.items():
                gs = game.copy()
                gs.execute_moves(move)
                d1 = gs.dead

                gs = game.copy()
                gs.dangerously_drop_piece(piece_data)
                d2 = gs.dead
                self.assertEqual(d1, d2)

            random_move = random.choice(list(moves.values()))
            game.execute_moves(random_move)
        print(f"Games tested: {games}")


if __name__ == "__main__":
    unittest.main()
