from typing import Optional, List, Dict, Literal, Set


from .pieces import I_WALLKICKS, WALLKICKS
from .models import Board, Piece, PieceData, Command
from .utils import check_collision, check_immobile, create_piece

Move = List[Command]

def generate_moves(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int):

    generated_moves: Dict[PieceData, Move] = dict()
    visited: Set[PieceData] = set()

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if not check_collision(board, current_piece, board_width):
        generate_move_helper(board, current_piece, generated_moves, board_height, board_width, [], visited)
        alternative_piece: Optional[PieceData] = create_piece(alternative, board_height, board_width) if alternative else None
        if (alternative_piece is not None) and (not check_collision(board, alternative_piece, board_width)):
            visited = set()
            generate_move_helper(board, alternative_piece, generated_moves, board_height, board_width, [], visited)

    return generated_moves

def move_left(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    current: PieceData = PieceData(piece.piece, piece.x - 1, piece.y, piece.rotation)
    if check_collision(board, current, board_width):
        return None
    return current

def move_right(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    current: PieceData = PieceData(piece.piece, piece.x + 1, piece.y, piece.rotation)
    if check_collision(board, current, board_width):
        return None
    return current

def move_down(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    current: PieceData = PieceData(piece.piece, piece.x, piece.y - 1, piece.rotation)
    if check_collision(board, current, board_width):
        return None
    return current


def sonic_drop(board: Board, piece: PieceData, board_width: int) -> PieceData:
    while True:
        current: PieceData = PieceData(piece.piece, piece.x, piece.y - 1, piece.rotation)
        if check_collision(board, current, board_width):
            return piece
        piece = current

def rotate_cw(board: Board, current: PieceData, board_width: int) -> Optional[PieceData]:
    initial_rotation: Literal[0, 1, 2, 3] = current.rotation
    new_rotation: Literal[0, 1, 2, 3] = (initial_rotation + 1) % 4
    
    wallkicks = I_WALLKICKS if current.piece == 'I' else WALLKICKS
    kick_data = wallkicks[initial_rotation][new_rotation]

    for dx, dy in kick_data:
        test_piece: PieceData = PieceData(current.piece, current.x + dx, current.y + dy, new_rotation)
        if not check_collision(board, test_piece, board_width):
            return test_piece

    return None

def rotate_ccw(board: Board, current: PieceData, board_width: int) -> Optional[PieceData]:
    initial_rotation: Literal[0, 1, 2, 3] = current.rotation
    new_rotation: Literal[0, 1, 2, 3] = (initial_rotation + 3) % 4

    wallkicks = I_WALLKICKS if current.piece == 'I' else WALLKICKS
    kick_data = wallkicks[initial_rotation][new_rotation]

    for dx, dy in kick_data:
        test_piece: PieceData = PieceData(current.piece, current.x + dx, current.y + dy, new_rotation)
        if not check_collision(board, test_piece, board_width):
            return test_piece

    return None

def add_move(board: Board, generated_moves: Dict[PieceData, Move], piece: PieceData, move: Move, board_width: int):
    current_piece = sonic_drop(board, piece, board_width)
    if (current_piece not in generated_moves) or (len(move) < len(generated_moves[current_piece])):
        generated_moves[current_piece] = move

def generate_move_helper(board: Board, current_piece: PieceData, generated_moves: Dict[PieceData, Move], board_height: int, board_width: int, move: Move, visited: Set[PieceData]):
    if current_piece in visited:
        return
    visited.add(current_piece)

    add_move(board, generated_moves, current_piece, move, board_width)

    move_left_piece: Optional[PieceData] = move_left(board, current_piece, board_width)
    if move_left_piece:
        generate_move_helper(board, move_left_piece, generated_moves, board_height, board_width, move + ['move_left'], visited)

    move_right_piece: Optional[PieceData] = move_right(board, current_piece, board_width)
    if move_right_piece:
        generate_move_helper(board, move_right_piece, generated_moves, board_height, board_width, move + ['move_right'], visited)

    move_down_piece: Optional[PieceData] = move_down(board, current_piece, board_width)
    if move_down_piece:
        generate_move_helper(board, move_down_piece, generated_moves, board_height, board_width, move + ['move_down'], visited)

    rotate_cw_piece: Optional[PieceData] = rotate_cw(board, current_piece, board_width)
    if rotate_cw_piece:
        generate_move_helper(board, rotate_cw_piece, generated_moves, board_height, board_width, move + ['rotate_cw'], visited)

    rotate_ccw_piece: Optional[PieceData] = rotate_ccw(board, current_piece, board_width)
    if rotate_ccw_piece:
        generate_move_helper(board, rotate_ccw_piece, generated_moves, board_height, board_width, move + ['rotate_ccw'], visited)

        