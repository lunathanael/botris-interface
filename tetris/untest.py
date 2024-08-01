import unittest
from env import TetrisEnv
from utils import generate_bag, Block, render_board, generate_garbage
from piece import Piece

class TestTetrisEnv(unittest.TestCase):

    def setUp(self):
        self.env = TetrisEnv()
    
    def test_sonic_drop(self):
        self.env.reset()
        self.env.game_state = self.env.game_state.create_game_state(TetrisEnv.get_default_options(), [Piece.I])
        self.env.step('sonic_drop')
        self.assertEqual(self.env.game_state.current.y, 1)

    def test_move_horizontally(self):
        self.env.reset()
        self.env.game_state = self.env.game_state.create_game_state(TetrisEnv.get_default_options(), [Piece.I])
        self.assertEqual(self.env.game_state.current.x, 3)
        
        self.env.step('move_right')
        self.assertEqual(self.env.game_state.current.x, 4)

        self.env.step('sonic_left')
        self.assertEqual(self.env.game_state.current.x, 0)
        
        self.env.step('move_left')
        self.assertEqual(self.env.game_state.current.x, 0)

    def test_hard_drop(self):
        self.env.reset()
        self.env.game_state = self.env.game_state.create_game_state(TetrisEnv.get_default_options(), [Piece.I])
        self.env.step('hard_drop')
        expected_board = [
            [None, None, None, "I", "I", "I", "I", None, None, None]
        ]

        self.assertEqual([[j.piece_type if j else j for j in i] for i in self.env.game_state.board], expected_board)

    def test_tspin(self):
        self.env.reset()
        self.env.game_state = self.env.game_state.create_game_state(TetrisEnv.get_default_options(), [Piece.T])
        tspin_setup = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, "G", None, None, None, None, None, None],
            ["G", "G", "G", None, None, None, "G", "G", "G", "G"],
            ["G", "G", "G", "G", None, "G", "G", "G", "G", "G"]
        ]

        tspin_setup = [[Block(j) if j else j for j in i] for i in tspin_setup]
        tspin_setup.reverse()
        self.env.game_state.board = tspin_setup
        
        self.env.step('rotate_cw')
        self.env.step('sonic_drop')
        self.env.step('rotate_cw')
        new_game_state, events = self.env.step('hard_drop')
        
        score_event = next((event for event in events if event.type == 'piece_placed'), None)
        self.assertIsNotNone(score_event)
        self.assertTrue('clear' in score_event.payload)
        self.assertEqual(score_event.payload['clear']['clear_name'], 'All-Spin Double')

    def test_tspin_wallkick(self):
        self.env.reset()
        self.env.game_state = self.env.game_state.create_game_state(TetrisEnv.get_default_options(), [Piece.T])
        tspin_setup = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, "G", None, None, "G", None, None, None],
            ["G", "G", "G", None, None, None, "G", "G", "G", "G"],
            ["G", "G", "G", "G", None, "G", "G", "G", "G", "G"]
        ]
        tspin_setup.reverse()
        self.env.game_state.board = tspin_setup
        
        self.env.step('move_right')
        self.env.step('rotate_ccw')
        self.env.step('sonic_drop')
        self.env.step('rotate_ccw')
        new_game_state, events = self.env.step('hard_drop')
        
        score_event = next((event for event in events if event.type == 'piece_placed'), None)
        self.assertIsNotNone(score_event)
        self.assertTrue('clear' in score_event.payload)
        self.assertEqual(score_event.payload['clear']['clear_name'], 'All-Spin Double')

    def test_add_garbage(self):
        self.env.reset()
        garbage_indices = generate_garbage(4, TetrisEnv.get_default_options())

        game_state = self.env.game_state.queue_garbage(garbage_indices)

        
        self.assertFalse(len(game_state.board) > 0 and any(block == "G" for block in game_state.board[0]))
        game_state, _ = self.env.step('hard_drop')
        self.assertTrue(any(block == "G" for block in game_state.board[0]))
        self.assertTrue(any(block == "G" for block in game_state.board[3]))

if __name__ == '__main__':
    unittest.main()
