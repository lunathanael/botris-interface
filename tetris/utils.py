from __future__ import annotations
import random
from typing import List, Tuple, Dict, Any, TYPE_CHECKING
from piece import Piece, PieceData, PIECE_MATRICES, WALL_KICKS, I_WALL_KICKS

if TYPE_CHECKING:
    from game_state import Block, GameState, Command, GameEvent


class Block:
    def __init__(self, piece_type: str = None):
        self.piece_type = piece_type

def generate_bag() -> List[str]:
    bag = Piece.all_pieces()
    random.shuffle(bag)
    return bag

def spawn_piece(board: List[List[Block]], piece: str, options: Dict[str, Any]) -> Tuple[PieceData, bool]:
    x = options['board_width'] // 2 - len(PIECE_MATRICES[piece][0]) // 2
    y = options['board_height']
    piece_data = PieceData(piece, x, y, 0)

    if check_collision(board, piece_data, options):
        return piece_data, True
    return piece_data, False

def rotate_matrix(matrix: List[List[Any]], rotation: int) -> List[List[Any]]:
    for _ in range(rotation):
        matrix = list(zip(*matrix[::-1]))
    return [list(row) for row in matrix]

def get_piece_matrix(piece: str, rotation: int) -> List[List[str]]:
    return rotate_matrix(PIECE_MATRICES[piece], rotation)

def check_collision(board: List[List[Block]], piece_data: PieceData, options: Dict[str, Any]) -> bool:
    piece_matrix = get_piece_matrix(piece_data.piece, piece_data.rotation)
    for y, row in enumerate(piece_matrix):
        for x, cell in enumerate(row):
            if cell:
                board_x = piece_data.x + x
                board_y = piece_data.y - y
                if (board_x < 0 or board_x >= options['board_width'] or
                    board_y < 0 or
                    (board_y < len(board) and board[board_y][board_x])):
                    return True
    return False

def try_wall_kicks(board: List[List[Block]], piece_data: PieceData, new_rotation: int, options: Dict[str, Any]) -> Tuple[PieceData, bool]:
    kicks = I_WALL_KICKS if piece_data.piece == Piece.I else WALL_KICKS
    kick_data = kicks[f"{piece_data.rotation}-{new_rotation}"]

    for dx, dy in kick_data:
        new_piece_data = PieceData(piece_data.piece, piece_data.x + dx, piece_data.y + dy, new_rotation)
        if not check_collision(board, new_piece_data, options):
            return new_piece_data, True
    return piece_data, False

def place_piece(board: List[List[Block]], piece_data: PieceData, options: Dict[str, Any]) -> List[List[Block]]:
    piece_matrix = get_piece_matrix(piece_data.piece, piece_data.rotation)
    new_board = [row[:] for row in board]
    
    for y, row in enumerate(piece_matrix):
        for x, cell in enumerate(row):
            if cell:
                board_y = piece_data.y - y
                board_x = piece_data.x + x
                while board_y >= len(new_board):
                    new_board.append([None] * options['board_width'])
                new_board[board_y][board_x] = Block(cell)
    
    return new_board

def clear_lines(board: List[List[Block]]) -> Tuple[List[List[Block]], List[Dict[str, Any]]]:
    cleared_lines = []
    new_board = []
    
    for y, row in enumerate(board):
        if all(block for block in row):
            cleared_lines.append({'height': y, 'blocks': row})
        else:
            new_board.append(row)
    
    lines_cleared = len(cleared_lines)
    new_board = [[None] * len(board[0]) for _ in range(lines_cleared)] + new_board
    
    return new_board, cleared_lines

def check_pc(board: List[List[Block]]) -> bool:
    return len(board) == 0 or all(all(block is None for block in row) for row in board)

def calculate_score(score_data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
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
        return {
            'score': score,
            'b2b': False,
            'combo': 0,
            'clear_name': None,
            'all_spin': False
        }

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
        elif lines_cleared == 2:
            score += attack_table['double']
            clear_name = 'Double'
        elif lines_cleared == 3:
            score += attack_table['triple']
            clear_name = 'Triple'
        elif lines_cleared == 4:
            score += attack_table['quad']
            clear_name = 'Quad'
            is_b2b_clear = True

    if b2b and is_b2b_clear:
        score += attack_table['b2b']

    if new_combo > 0:
        score += combo_table[min(new_combo, len(combo_table) - 1)]

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

def generate_garbage(damage: int, options: Dict[str, Any]) -> List[int]:
    hole_indices = []
    hole_index = None

    for _ in range(damage):
        if hole_index is None or random.random() < options['garbage_messiness']:
            hole_index = random.randint(0, options['board_width'] - 1)
        hole_indices.append(hole_index)

    return hole_indices

def add_garbage(board: List[List[Block]], hole_indices: List[int], options: Dict[str, Any]) -> List[List[Block]]:
    new_board = [row[:] for row in board]
    for hole_index in hole_indices:
        garbage_line = [Block('G') for _ in range(options['board_width'])]
        garbage_line[hole_index] = None
        new_board.insert(0, garbage_line)
    return new_board

def get_board_heights(board: List[List[Block]], options: Dict[str, Any]) -> List[int]:
    if not board:
        return [0] * options['board_width']

    heights = []
    for x in range(options['board_width']):
        for y in range(len(board) - 1, -1, -1):
            if board[y][x]:
                heights.append(y + 1)
                break
        else:
            heights.append(0)

    return heights

def render_board(board: List[List[Block]], current_piece: PieceData = None):
    # ANSI color codes
    COLORS = {
        'I': '\033[96m',  # Cyan
        'O': '\033[93m',  # Yellow
        'T': '\033[95m',  # Magenta
        'S': '\033[92m',  # Green
        'Z': '\033[91m',  # Red
        'J': '\033[94m',  # Blue
        'L': '\033[97m',  # White
        'G': '\033[90m',  # Gray (for garbage)
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'

    # Add current piece to the board view
    if current_piece:
        piece_matrix = get_piece_matrix(current_piece.piece, current_piece.rotation)
        for y, row in enumerate(piece_matrix):
            for x, cell in enumerate(row):
                if cell:
                    board_y = current_piece.y - y
                    board_x = current_piece.x + x
                    if 0 <= board_y < len(board) and 0 <= board_x < len(board[0]):
                        board[board_y][board_x] = Block(current_piece.piece)

    # Render the board
    border = f"{BOLD}+{'--' * len(board[0])}+{RESET}"
    rendered_board = [border]
    for row in reversed(board):
        line = f"{BOLD}|{RESET}"
        for block in row:
            if block:
                line += f"{COLORS.get(block.piece_type, '')}{BOLD}██{RESET}"
            else:
                line += "  "
        line += f"{BOLD}|{RESET}"
        rendered_board.append(line)
    rendered_board.append(border)

    print('\n'.join(rendered_board))

    # Clear the current piece from the board if it was added
    if current_piece:
        piece_matrix = get_piece_matrix(current_piece.piece, current_piece.rotation)
        for y, row in enumerate(piece_matrix):
            for x, cell in enumerate(row):
                if cell:
                    board_y = current_piece.y - y
                    board_x = current_piece.x + x
                    if 0 <= board_y < len(board) and 0 <= board_x < len(board[0]):
                        board[board_y][board_x] = None

def queue_garbage(game_state: GameState, hole_indices: List[int]) -> GameState:
    new_game_state = GameState()
    new_game_state.__dict__.update(game_state.__dict__)
    new_game_state.garbage_queue.extend(hole_indices)
    return new_game_state

def get_board_bumpiness(board: List[List[Block]], options: Dict[str, Any]) -> float:
    heights = get_board_heights(board, options)
    avg_height = sum(heights) / len(heights)
    variance = sum((h - avg_height) ** 2 for h in heights) / len(heights)
    return (variance ** 0.5)

def get_board_avg_height(board: List[List[Block]], options: Dict[str, Any]) -> float:
    heights = get_board_heights(board, options)
    return sum(heights) / len(heights)

def check_immobile(board: List[List[Block]], piece_data: PieceData, options: Dict[str, Any]) -> bool:
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_piece_data = PieceData(piece_data.piece, piece_data.x + dx, piece_data.y + dy, piece_data.rotation)
        if not check_collision(board, new_piece_data, options):
            return False
    return True

# def execute_commands(game_state: GameState, commands: List[Command], options: Dict[str, Any]) -> Tuple[GameState, List[GameEvent]]:
#     new_game_state = game_state
#     all_events = []

#     for command in commands:
#         new_game_state, events = execute_command(new_game_state, command, options)
#         all_events.extend(events)

#     return new_game_state, all_events