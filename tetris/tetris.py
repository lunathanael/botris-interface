import colorama
from colorama import Fore, Back, Style

from pieces import generate_bag, get_piece_matrix, WALLKICKS, I_WALLKICKS
from utils import (
    check_collision, check_immobile, place_piece, clear_lines,
    check_pc, calculate_score, generate_garbage, add_garbage,
    get_board_heights, get_board_bumpiness, get_board_avg_height
)

DEFAULT_OPTIONS = {
    'board_width': 10,
    'board_height': 20,
    'garbage_messiness': 0.05,
    'attack_table': {
        'single': 0,
        'double': 1,
        'triple': 2,
        'quad': 4,
        'asd': 4,
        'ass': 2,
        'ast': 6,
        'pc': 10,
        'b2b': 1,
    },
    'combo_table': [0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
}

class TetrisGame:
    def __init__(self, options=None):
        self.options = {**DEFAULT_OPTIONS, **(options or {})}
        self.reset()

    def reset(self):
        self.board = []
        self.queue = generate_bag()
        self.garbage_queue = []
        self.held = None
        self.current = self.spawn_piece()
        self.is_immobile = False
        self.can_hold = True
        self.combo = 0
        self.b2b = False
        self.score = 0
        self.pieces_placed = 0
        self.dead = False

    def spawn_piece(self):
        piece = self.queue.pop(0)
        if len(self.queue) < 6:
            self.queue.extend(generate_bag())
        
        x = self.options['board_width'] // 2 - ((len(get_piece_matrix(piece, 0)[0]) + 1) // 2)
        y = self.options['board_height']
        
        return {'piece': piece, 'x': x, 'y': y, 'rotation': 0}

    def get_public_state(self):
        return {
            'board': self.board,
            'queue': self.queue[:6],
            'garbage_queued': len(self.garbage_queue),
            'held': self.held,
            'current': self.current,
            'is_immobile': self.is_immobile,
            'can_hold': self.can_hold,
            'combo': self.combo,
            'b2b': self.b2b,
            'score': self.score,
            'pieces_placed': self.pieces_placed,
            'dead': self.dead,
        }

    def execute_command(self, command):
        if self.dead:
            raise ValueError("Cannot act when dead")

        events = []

        if command == 'move_left':
            self.current['x'] -= 1
            if check_collision(self.board, self.current, self.options):
                self.current['x'] += 1
        elif command == 'move_right':
            self.current['x'] += 1
            if check_collision(self.board, self.current, self.options):
                self.current['x'] -= 1
        elif command == 'sonic_left':
            while not check_collision(self.board, self.current, self.options):
                self.current['x'] -= 1
            self.current['x'] += 1
        elif command == 'sonic_right':
            while not check_collision(self.board, self.current, self.options):
                self.current['x'] += 1
            self.current['x'] -= 1
        elif command == 'drop':
            self.current['y'] -= 1
            if check_collision(self.board, self.current, self.options):
                self.current['y'] += 1
        elif command == 'sonic_drop':
            while not check_collision(self.board, self.current, self.options):
                self.current['y'] -= 1
            self.current['y'] += 1
        elif command == 'hard_drop':
            initial_piece_state = self.current.copy()
            while not check_collision(self.board, self.current, self.options):
                self.current['y'] -= 1
            self.current['y'] += 1
            final_piece_state = self.current.copy()

            self.board = place_piece(self.board, self.current, self.options)
            self.board, cleared_lines = clear_lines(self.board)
            pc = check_pc(self.board)

            score_data = calculate_score({
                'pc': pc,
                'lines_cleared': len(cleared_lines),
                'is_immobile': self.is_immobile,
                'b2b': self.b2b,
                'combo': self.combo,
            }, self.options)

            self.combo = score_data['combo']
            self.b2b = score_data['b2b']

            self.score += score_data['score']
            self.pieces_placed += 1

            attack = score_data['score']
            cancelled = 0
            while self.garbage_queue and attack > 0:
                self.garbage_queue.pop(0)
                attack -= 1
                cancelled += 1

            tanked_lines = []
            if not cleared_lines:
                hole_indices = self.garbage_queue
                self.board = add_garbage(self.board, hole_indices, self.options)
                tanked_lines = hole_indices
                self.garbage_queue = []

            events.append({
                'type': 'piece_placed',
                'payload': {
                    'initial': initial_piece_state,
                    'final': final_piece_state,
                }
            })

            if score_data['clear_name']:
                events.append({
                    'type': 'clear',
                    'payload': {
                        'clear_name': score_data['clear_name'],
                        'all_spin': score_data['all_spin'],
                        'b2b': score_data['b2b'],
                        'combo': score_data['combo'],
                        'pc': pc,
                        'attack': attack,
                        'cancelled': cancelled,
                        'piece': final_piece_state,
                        'cleared_lines': cleared_lines,
                    }
                })

            if tanked_lines:
                events.append({
                    'type': 'damage_tanked',
                    'payload': {
                        'hole_indices': tanked_lines,
                    }
                })

            self.current = self.spawn_piece()
            self.can_hold = True
            self.is_immobile = check_immobile(self.board, self.current, self.options)
            
            if check_collision(self.board, self.current, self.options):
                self.dead = True
                events.append({'type': 'game_over'})

        elif command in ['rotate_cw', 'rotate_ccw']:
            initial_rotation = self.current['rotation']
            new_rotation = (initial_rotation + (1 if command == 'rotate_cw' else 3)) % 4
            
            wallkicks = I_WALLKICKS if self.current['piece'] == 'I' else WALLKICKS
            kick_data = wallkicks[f"{initial_rotation}-{new_rotation}"]
            
            for dx, dy in kick_data:
                test_piece = self.current.copy()
                test_piece['rotation'] = new_rotation
                test_piece['x'] += dx
                test_piece['y'] += dy
                if not check_collision(self.board, test_piece, self.options):
                    self.current = test_piece
                    self.is_immobile = check_immobile(self.board, self.current, self.options)
                    break

        elif command == 'hold':
            if not self.can_hold:
                return {'events': []}

            new_held = self.current['piece']
            if self.held:
                self.current = self.spawn_piece()
                self.current['piece'] = self.held
            else:
                self.current = self.spawn_piece()
            
            self.held = new_held
            self.can_hold = False
            self.is_immobile = check_immobile(self.board, self.current, self.options)
            
            if check_collision(self.board, self.current, self.options):
                self.dead = True
                events.append({'type': 'game_over'})

        return {'events': events}

    def queue_garbage(self, hole_indices):
        self.garbage_queue.extend(hole_indices)

    def print_board(self):
        rendered_board = [['.' if cell is None else cell for cell in row] for row in self.board]
        rendered_board.reverse()
        for row in rendered_board:
            print(''.join(row))
        print()

    def get_board_stats(self):
        return {
            'heights': get_board_heights(self.board, self.options),
            'bumpiness': get_board_bumpiness(self.board, self.options),
            'avg_height': get_board_avg_height(self.board, self.options),
        }
    
    def render_board(self):
        t_board = self.board.copy()
        self.board = place_piece(self.board, self.current, self.options)
        colorama.init()
        color_map = {
            'I': Fore.CYAN,
            'O': Fore.YELLOW,
            'T': Fore.MAGENTA,
            'S': Fore.GREEN,
            'Z': Fore.RED,
            'J': Fore.BLUE,
            'L': Fore.WHITE,
            'G': Fore.BLACK + Back.WHITE
        }

        print('┌' + '──' * self.options['board_width'] + '┐')

        for y in range(self.options['board_height'] - 1, -1, -1):
            print('│', end='')
            for x in range(self.options['board_width']):
                if y < len(self.board) and self.board[y][x] is not None:
                    piece = self.board[y][x]
                    print(f'{color_map[piece]}██{Style.RESET_ALL}', end='')
                else:
                    print('  ', end='')
            print('│', end='')

            if y == self.options['board_height'] - 1:
                print(f'  Score: {self.score}')
            elif y == self.options['board_height'] - 3:
                print(f'  Combo: {self.combo}')
            elif y == self.options['board_height'] - 5:
                print(f'  B2B: {"Yes" if self.b2b else "No"}')
            elif y == self.options['board_height'] - 7:
                print(f'  Pieces: {self.pieces_placed}')
            elif y == self.options['board_height'] - 9:
                print(f'  Hold: {self.held or "Empty"}')
            else:
                print()

        print('└' + '──' * self.options['board_width'] + '┘')

        print(f'\nCurrent piece: {self.current["piece"]}')
        piece_matrix = get_piece_matrix(self.current['piece'], self.current['rotation'])
        for row in piece_matrix:
            print('  ' + ''.join([f'{color_map[cell]}██{Style.RESET_ALL}' if cell else '  ' for cell in row]))

        print('\nNext pieces:')
        for i, piece in enumerate(self.queue[:5]):
            if i > 0:
                print()
            print(f'  {piece}:')
            piece_matrix = get_piece_matrix(piece, 0)
            for row in piece_matrix:
                print('    ' + ''.join([f'{color_map[cell]}██{Style.RESET_ALL}' if cell else '  ' for cell in row]))

        print(f'\nGarbage queued: {len(self.garbage_queue)}')
        self.board = t_board

if __name__ == "__main__":
    game = TetrisGame()
    
    game.execute_command('move_right')
    game.execute_command('hard_drop')
    game.execute_command('rotate_cw')
    game.execute_command('move_left')
    game.execute_command('hard_drop')
    
    # Print the current state
    print("Current game state:")
    game.render_board()
    
    # Print some stats
    print("Board stats:", game.get_board_stats())
    
    # Print the public game state
    print("Public game state:", game.get_public_state())