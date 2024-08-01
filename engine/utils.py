import random

from .pieces import I_WALLKICKS, WALLKICKS, get_piece_matrix


def check_collision(board, piece_data, options):
    piece_matrix = get_piece_matrix(piece_data['piece'], piece_data['rotation'])
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell:
                board_x = piece_data['x'] + piece_x
                board_y = piece_data['y'] - piece_y
                if (board_x < 0 or board_x >= options['board_width'] or
                    board_y < 0 or (board_y < len(board) and board[board_y][board_x])):
                    return True
    return False

def check_immobile(board, piece_data, options):
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_piece_data = piece_data.copy()
        new_piece_data['x'] += dx
        new_piece_data['y'] += dy
        if not check_collision(board, new_piece_data, options):
            return False
    return True

def place_piece(board, piece_data, options):
    piece_matrix = get_piece_matrix(piece_data['piece'], piece_data['rotation'])
    new_board = [row[:] for row in board]
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell:
                board_x = piece_data['x'] + piece_x
                board_y = piece_data['y'] - piece_y
                while board_y >= len(new_board):
                    new_board.append([None] * options['board_width'])
                new_board[board_y][board_x] = cell
    return new_board

def clear_lines(board):
    cleared_lines = []
    new_board = [row for row in board if not all(cell is not None for cell in row)]
    cleared_lines = [{'height': i, 'blocks': row} for i, row in enumerate(board) if all(cell is not None for cell in row)]
    return new_board, cleared_lines

def check_pc(board):
    return len(board) == 0 or all(all(cell is None for cell in row) for row in board)

def calculate_score(score_data, options):
    lines_cleared = score_data['lines_cleared']
    is_immobile = score_data['is_immobile']
    b2b = score_data['b2b']
    combo = score_data['combo']
    pc = score_data['pc']

    attack_table = options['attack_table']
    combo_table = options['combo_table']

    score = 0
    is_b2b_clear = False
    clear_name = None
    all_spin = False

    if lines_cleared == 0:
        return {'score': 0, 'b2b': False, 'combo': 0, 'clear_name': None, 'all_spin': False}

    new_combo = combo + 1

    if is_immobile:
        all_spin = True
        is_b2b_clear = True
        if lines_cleared == 1:
            score += attack_table['ass']
            clear_name = 'All-Spin Single'
        elif lines_cleared == 2:
            score += attack_table['asd']
            clear_name = 'All-Spin Double'
        elif lines_cleared == 3:
            score += attack_table['ast']
            clear_name = 'All-Spin Triple'
    else:
        if lines_cleared == 1:
            score += attack_table['single']
            clear_name = 'Single'
            is_b2b_clear = False
        elif lines_cleared == 2:
            score += attack_table['double']
            clear_name = 'Double'
            is_b2b_clear = False
        elif lines_cleared == 3:
            score += attack_table['triple']
            clear_name = 'Triple'
            is_b2b_clear = False
        elif lines_cleared == 4:
            score += attack_table['quad']
            clear_name = 'Quad'
            is_b2b_clear = True

    if b2b and is_b2b_clear:
        score += attack_table['b2b']

    if new_combo > 0:
        combo_index = min(new_combo - 1, len(combo_table) - 1)
        score += combo_table[combo_index]

    if pc:
        score = attack_table['pc']
        clear_name = 'Perfect Clear'

    return {
        'score': score,
        'b2b': is_b2b_clear,
        'combo': new_combo,
        'clear_name': clear_name,
        'all_spin': all_spin
    }

def generate_garbage(damage, options):
    hole_indices = []
    hole_index = None

    for _ in range(damage):
        if hole_index is None or random.random() < options['garbage_messiness']:
            hole_index = random.randint(0, options['board_width'] - 1)
        hole_indices.append(hole_index)

    return hole_indices

def add_garbage(board, hole_indices, options):
    new_board = [row[:] for row in board]
    for hole_index in hole_indices:
        line = ['G'] * options['board_width']
        line[hole_index] = None
        new_board.insert(0, line)
    return new_board

def get_board_heights(board, options):
    if not board:
        return [0] * options['board_width']

    heights = []
    for x in range(options['board_width']):
        y = len(board) - 1
        while y >= 0 and board[y][x] is None:
            y -= 1
        heights.append(y + 1)

    return heights

def get_board_bumpiness(board, options):
    heights = get_board_heights(board, options)
    avg_height = sum(heights) / len(heights)
    variance = sum((h - avg_height) ** 2 for h in heights) / len(heights)
    return (variance ** 0.5)

def get_board_avg_height(board, options):
    heights = get_board_heights(board, options)
    return sum(heights) / len(heights)
