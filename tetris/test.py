# test_tetris.py

import unittest
from tetris import TetrisGame
from pieces import generate_bag
from utils import generate_garbage

class TestTetrisGame(unittest.TestCase):
    def test_sonic_drop(self):
        game = TetrisGame()
        game.queue = ['I']
        game.current = game.spawn_piece()
        game.execute_command('sonic_drop')
        self.assertEqual(game.current['y'], 1)

    def test_move_horizontally(self):
        game = TetrisGame()
        game.queue = ['I']
        game.current = game.spawn_piece()
        self.assertEqual(game.current['x'], 3)
        game.execute_command('move_right')
        self.assertEqual(game.current['x'], 4)
        game.execute_command('sonic_left')
        self.assertEqual(game.current['x'], 0)
        game.execute_command('move_left')
        self.assertEqual(game.current['x'], 0)

    def test_hard_drop(self):
        game = TetrisGame()
        game.queue = ['I']
        game.current = game.spawn_piece()
        game.execute_command('hard_drop')
        expected_board = [[None] * 3 + ['I'] * 4 + [None] * 3]
        self.assertEqual(game.board, expected_board)

    def test_tspin(self):
        game = TetrisGame()
        game.queue = ['T']
        game.current = game.spawn_piece()
        tspin_setup = [
            [None] * 10,
            [None] * 3 + ['G'] + [None] * 2 + ['G'] + [None] * 3,
            ['G'] * 3 + [None] * 3 + ['G'] * 4,
            ['G'] * 4 + [None] + ['G'] * 5,
        ]
        tspin_setup.reverse()
        game.board = tspin_setup
        game.execute_command('rotate_cw')
        game.execute_command('sonic_drop')
        game.execute_command('rotate_cw')
        result = game.execute_command('hard_drop')
        self.assertTrue(any([event['type'] == 'clear' for event in result['events']]))
        clear_event = next((event for event in result['events'] if event['type'] == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event['payload']['attack'], 4)
        self.assertEqual(clear_event['payload']['clear_name'], 'All-Spin Double')

    def test_tspin_wallkick(self):
        game = TetrisGame()
        game.queue = ['T']
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
        self.assertTrue(any([event['type'] == 'clear' for event in result['events']]))
        clear_event = next((event for event in result['events'] if event['type'] == 'clear'), None)
        self.assertIsNotNone(clear_event)
        self.assertEqual(clear_event['payload']['attack'], 4)
        self.assertEqual(clear_event['payload']['clear_name'], 'All-Spin Double')

    def test_add_garbage(self):
        game = TetrisGame()
        garbage_indices = generate_garbage(4, game.options)
        game.queue_garbage(garbage_indices)
        self.assertFalse(any('G' in row for row in game.board))
        game.execute_command('hard_drop')
        self.assertTrue('G' in game.board[0])
        self.assertTrue('G' in game.board[3])

if __name__ == '__main__':
    unittest.main()