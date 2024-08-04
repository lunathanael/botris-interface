import copy
import math
import random
from typing import Dict, List, Optional, Tuple

from .models import (AttackTable, Block, Board, ClearName, PieceData,
                     ScoreData, ScoreInfo, Piece, Command)
from .pieces import PieceMatrix, get_piece_matrix, get_piece_mask, get_matrix_mask

def get_subgrid(board: Board, start_x: int, start_y: int) -> Tuple[Tuple[int]]:
    subgrid = tuple(
        tuple(
            board[y][x] if y < len(board) and x < len(board[y]) else None
            for x in range(start_x, start_x + 3)
        )
        for y in range(start_y + 2, start_y - 1 , -1)
    )
    return subgrid

def check_collision(board: Board, piece_data: PieceData, board_width: int) -> bool:
    piece_x_start = piece_data.x
    piece_y_start = piece_data.y - 2
    if (piece_x_start < 0) or (piece_x_start + 2 >= board_width) or (piece_y_start < 0):
        return True
    board_height = len(board)
    if piece_y_start >= board_height:
        if _check_collision(board, piece_data, board_width):
            print("FALSE NEGATIVE")
            print(f'Board: {board}')
            print(f'Piece: {piece_data}')
        return False
    subgrid = get_subgrid(board, piece_x_start, piece_y_start)
    board_mask = get_matrix_mask(subgrid)
    piece_mask = get_piece_mask(piece_data.piece, piece_data.rotation)
        
    if piece_mask & board_mask:
        if not _check_collision(board, piece_data, board_width):
            print("FALSE POSITIVE")
            print(f'Board: {board}')
            print(f'Piece: {piece_data}')
            print(f'Subgrid: {subgrid}')
            print(f'Piece mask: {piece_mask}')
            print(f'Board mask: {board_mask}')
        return True
    if _check_collision(board, piece_data, board_width):
        print("FALSE NEGATIVE")
        print(f'Board: {board}')
        print(f'Piece: {piece_data}')
        print(f'Subgrid: {subgrid}')
        print(f'Piece mask: {piece_mask}')
        print(f'Board mask: {board_mask}')
        #render mask
        for row in range(3):
            for col in range(3):
                if piece_mask & (1 << (row * 3 + col)):
                    print('X', end='')
                else:
                    print('O', end='')
            print()
        for row in range(3):
            for col in range(3):
                if board_mask & (1 << (row * 3 + col)):
                    print('X', end='')
                else:
                    print('O', end='')
            print()
        
    return False

def _check_collision(board: Board, piece_data: PieceData, board_width: int) -> bool:
    piece_matrix: PieceMatrix = get_piece_matrix(piece_data.piece, piece_data.rotation)
    piece_x = piece_data.x
    piece_y = piece_data.y
    board_height = len(board)

    for matrix_y, row in enumerate(piece_matrix):
        for matrix_x, cell in enumerate(row):
            if cell:
                board_x = piece_x + matrix_x
                board_y = piece_y - matrix_y

                if board_x < 0 or board_x >= board_width or board_y < 0:
                    return True
                
                if board_y < board_height and board[board_y][board_x]:
                    return True

    return False

def check_immobile(board: Board, piece_data: PieceData, board_width: int) -> bool:
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        new_piece_data: PieceData = PieceData(piece_data.piece, piece_data.x + dx, piece_data.y + dy, piece_data.rotation)
        if not check_collision(board, new_piece_data, board_width):
            return False
    return True

def place_piece(board: Board, piece_data: PieceData, board_width: int) -> Board:
    piece_matrix: PieceMatrix = get_piece_matrix(piece_data.piece, piece_data.rotation)
    new_board: Board = copy.deepcopy(board)
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell:
                board_x: int = piece_data.x + piece_x
                board_y: int = piece_data.y - piece_y
                if board_y >= len(new_board):
                    diff: int = board_y - len(new_board) + 1
                    new_board.extend([[None] * board_width for _ in range(diff)])
                new_board[board_y][board_x] = cell
    return new_board

def clear_lines(board: Board) -> Tuple[Board, List[Dict[str, int | List[Block]]]]:
    new_board: Board = [row for row in board if not all(cell is not None for cell in row)]
    cleared_lines: List[Dict[str, int | List[Block]]] = [{'height': i, 'blocks': row} for i, row in enumerate(board) if all(cell is not None for cell in row)]
    return new_board, cleared_lines

def check_pc(board) -> bool:
    return len(board) == 0 or all(all(cell is None for cell in row) for row in board)

def calculate_score(score_info: ScoreInfo, attack_table: AttackTable, combo_table: List[int]) -> ScoreData:
    lines_cleared: int = score_info.lines_cleared
    is_immobile: bool = score_info.is_immobile
    b2b: bool = score_info.b2b
    combo: int = score_info.combo
    pc: bool = score_info.pc

    score: int = 0
    is_b2b_clear: bool = False
    clear_name: Optional[ClearName] = None
    all_spin: bool = False

    if lines_cleared == 0:
        return ScoreData(score=0, b2b=False, combo=0, clear_name=None, all_spin=False)

    new_combo: int = combo + 1

    if is_immobile:
        all_spin = True
        is_b2b_clear = True
        match lines_cleared:
            case 1:
                score += attack_table.ass
                clear_name = 'All-Spin Single'
            case 2:
                score += attack_table.asd
                clear_name = 'All-Spin Double'
            case 3:
                score += attack_table.ast
                clear_name = 'All-Spin Triple'
    else:
        match lines_cleared:
            case 1:
                score += attack_table.single
                clear_name = 'Single'
                is_b2b_clear = False
            case 2:
                score += attack_table.double
                clear_name = 'Double'
                is_b2b_clear = False
            case 3:
                score += attack_table.triple
                clear_name = 'Triple'
                is_b2b_clear = False
            case 4:
                score += attack_table.quad
                clear_name = 'Quad'
                is_b2b_clear = True

    if b2b and is_b2b_clear:
        score += attack_table.b2b

    if new_combo > 0:
        combo_index = min(new_combo - 1, len(combo_table) - 1)
        score += combo_table[combo_index]

    if pc:
        score = attack_table.pc
        clear_name = 'Perfect Clear'

    return ScoreData(score=score, b2b=is_b2b_clear, combo=new_combo, clear_name=clear_name, all_spin=all_spin)

def generate_garbage(damage: int, garbage_messiness: float, board_width: int) -> List[int]:
    hole_indices: List[int] = []
    hole_index: Optional[int] = None

    for _ in range(damage):
        if hole_index is None or random.random() < garbage_messiness:
            hole_index = math.floor(random.random() * board_width)
        hole_indices.append(hole_index)

    return hole_indices

def add_garbage(board: Board, hole_indices: List[int], board_width: int) -> Board:
    new_board: Board = copy.deepcopy(board)
    for hole_index in hole_indices:
        line: List[Block] = ['G'] * board_width
        line[hole_index] = None
        new_board.insert(0, line)
    return new_board

def get_board_heights(board: Board, board_width: int) -> List[int]:
    if not board:
        return [0] * board_width

    heights: List[int] = []
    for x in range(board_width):
        y: int = len(board) - 1
        while y >= 0 and board[y][x] is None:
            y -= 1
        heights.append(y + 1)
    return heights

def get_board_avg_height(board: Board, board_width: int) -> float:
    heights = get_board_heights(board, board_width)
    return sum(heights) / len(heights)


def get_board_bumpiness(board: Board, board_width: int) -> float:
    heights = get_board_heights(board, board_width)
    avg_height = sum(heights) / len(heights)
    variance: float = sum((h - avg_height) ** 2 for h in heights) / len(heights)
    return (variance ** 0.5)

def create_piece(piece: Piece, board_height: int, board_width: int) -> PieceData:
    x: int = board_width // 2 - ((len(get_piece_matrix(piece, 0)[0]) + 1) // 2)
    y: int = board_height
    return PieceData(piece=piece, x=x, y=y, rotation=0)

        