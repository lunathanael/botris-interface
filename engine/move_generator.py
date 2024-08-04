from typing import Optional, List, Dict, Literal, Set, Tuple, Deque, Literal

from heapq import heappop, heappush
from collections import deque


from .pieces import I_WALLKICKS, WALLKICKS
from .models import Board, Piece, PieceData, Command, Move
from .utils import check_collision, check_immobile, create_piece


def generate_moves(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int, algo: Literal['bfs', 'dfs', 'dijk', 'dijk-short']='dijk-short') -> Dict[PieceData, Move]:
    match algo:
        case 'bfs':
            return bfs_generate_moves(board, piece, alternative, board_height, board_width)
        case 'dfs':
            return dfs_generate_moves(board, piece, alternative, board_height, board_width)
        case 'dijk':
            return dijkstra_generate_moves(board, piece, alternative, board_height, board_width)
        case 'dijk-short':
            return dijkstra_generate_moves_short(board, piece, alternative, board_height, board_width)
        case _:
            raise ValueError(f"Invalid algorithm: {algo}")

def dfs_generate_moves(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int):

    generated_moves: Dict[PieceData, Move] = dict()
    visited: Set[PieceData] = set()

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if not check_collision(board, current_piece, board_width):
        dfs_generate_move_helper(board, current_piece, generated_moves, board_height, board_width, [], visited)
        alternative_piece: Optional[PieceData] = create_piece(alternative, board_height, board_width) if alternative else None
        if (alternative_piece is not None) and (not check_collision(board, alternative_piece, board_width)):
            visited = set()
            dfs_generate_move_helper(board, alternative_piece, generated_moves, board_height, board_width, ['hold'], visited)
    return generated_moves


def bfs_generate_moves(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int):

    generated_moves: Dict[PieceData, Move] = dict()

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if not check_collision(board, current_piece, board_width):
        bfs_generate_move_helper(board, current_piece, generated_moves, board_height, board_width, False)
        alternative_piece: Optional[PieceData] = create_piece(alternative, board_height, board_width) if alternative else None
        if (alternative_piece is not None) and (not check_collision(board, alternative_piece, board_width)):
            bfs_generate_move_helper(board, alternative_piece, generated_moves, board_height, board_width, True)
    return generated_moves

def dijkstra_generate_moves(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int):

    generated_moves: Dict[PieceData, Move] = dict()

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if not check_collision(board, current_piece, board_width):
        dijkstra_generate_move_helper(board, current_piece, generated_moves, board_height, board_width, False)
        alternative_piece: Optional[PieceData] = create_piece(alternative, board_height, board_width) if alternative else None
        if (alternative_piece is not None) and (not check_collision(board, alternative_piece, board_width)):
            dijkstra_generate_move_helper(board, alternative_piece, generated_moves, board_height, board_width, True)
    return generated_moves

def dijkstra_generate_moves_short(board: Board, piece: Piece, alternative: Optional[Piece], board_height: int, board_width: int):

    generated_moves: Dict[PieceData, Move] = dict()

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if not check_collision(board, current_piece, board_width):
        short_dijkstra_generate_move_helper(board, current_piece, generated_moves, board_height, board_width, False)
        alternative_piece: Optional[PieceData] = create_piece(alternative, board_height, board_width) if alternative else None
        if (alternative_piece is not None) and (not check_collision(board, alternative_piece, board_width)):
            short_dijkstra_generate_move_helper(board, alternative_piece, generated_moves, board_height, board_width, True)
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

def sonic_left(board: Board, piece: PieceData, board_width: int) -> PieceData:
    while True:
        current: PieceData = PieceData(piece.piece, piece.x - 1, piece.y, piece.rotation)
        if check_collision(board, current, board_width):
            return piece
        piece = current

def sonic_right(board: Board, piece: PieceData, board_width: int) -> PieceData:
    while True:
        current: PieceData = PieceData(piece.piece, piece.x + 1, piece.y, piece.rotation)
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
    piece = sonic_drop(board, piece, board_width)
    if (piece not in generated_moves) or (len(move) < len(generated_moves[piece])):
        generated_moves[piece] = move

def dfs_generate_move_helper(board: Board, current_piece: PieceData, generated_moves: Dict[PieceData, Move], board_height: int, board_width: int, move: Move, visited: Set[PieceData]):
    if current_piece in visited:
        return
    
    visited.add(current_piece)

    move_down_piece: Optional[PieceData] = move_down(board, current_piece, board_width)
    if move_down_piece is None:
        add_move(board, generated_moves, current_piece, move, board_width)
    else:
        dfs_generate_move_helper(board, move_down_piece, generated_moves, board_height, board_width, move + ['drop'], visited)

    move_left_piece: Optional[PieceData] = move_left(board, current_piece, board_width)
    if move_left_piece is not None:
        dfs_generate_move_helper(board, move_left_piece, generated_moves, board_height, board_width, move + ['move_left'], visited)
    move_right_piece: Optional[PieceData] = move_right(board, current_piece, board_width)
    if move_right_piece is not None:
        dfs_generate_move_helper(board, move_right_piece, generated_moves, board_height, board_width, move + ['move_right'], visited)

    rotate_cw_piece: Optional[PieceData] = rotate_cw(board, current_piece, board_width)
    if rotate_cw_piece is not None:
        dfs_generate_move_helper(board, rotate_cw_piece, generated_moves, board_height, board_width, move + ['rotate_cw'], visited)

    rotate_ccw_piece: Optional[PieceData] = rotate_ccw(board, current_piece, board_width)
    if rotate_ccw_piece is not None:
        dfs_generate_move_helper(board, rotate_ccw_piece, generated_moves, board_height, board_width, move + ['rotate_ccw'], visited)

def bfs_generate_move_helper(board: Board, current_piece: PieceData, generated_moves: Dict[PieceData, Move], board_height: int, board_width: int, held: bool=False):
    queue: Deque[Tuple[PieceData, Move]] = [(current_piece, ['hold'] if held else [])]
    visited: Set[PieceData] = set()

    while queue:
        current_piece, move = queue.pop(0)

        if current_piece in visited:
            continue

        visited.add(current_piece)

        move_down_piece: Optional[PieceData] = move_down(board, current_piece, board_width)
        if move_down_piece is None:
            add_move(board, generated_moves, current_piece, move, board_width)
        else:
            queue.append((move_down_piece, move + ['drop']))

        move_left_piece: Optional[PieceData] = move_left(board, current_piece, board_width)
        if move_left_piece is not None:
            queue.append((move_left_piece, move + ['move_left']))
        move_right_piece: Optional[PieceData] = move_right(board, current_piece, board_width)
        if move_right_piece is not None:
            queue.append((move_right_piece, move + ['move_right']))

        rotate_cw_piece: Optional[PieceData] = rotate_cw(board, current_piece, board_width)
        if rotate_cw_piece is not None:
            queue.append((rotate_cw_piece, move + ['rotate_cw']))

        rotate_ccw_piece: Optional[PieceData] = rotate_ccw(board, current_piece, board_width)
        if rotate_ccw_piece is not None:
            queue.append((rotate_ccw_piece, move + ['rotate_ccw']))

def dijkstra_generate_move_helper(board: Board, current_piece: PieceData, generated_moves: Dict[PieceData, Move], board_height: int, board_width: int, held: bool=False):
    priority_queue: List[Tuple[int, PieceData, Move]] = [(0, current_piece, ['hold'] if held else [])]
    visited: Set[PieceData] = set()
    distance: Dict[PieceData, int] = {current_piece: 0}

    while priority_queue:
        current_distance, current_piece, move = heappop(priority_queue)

        if current_piece in visited:
            continue

        visited.add(current_piece)

        move_down_piece: Optional[PieceData] = move_down(board, current_piece, board_width)
        if move_down_piece is not None:
            new_distance = current_distance + 1
            if move_down_piece not in distance or new_distance < distance[move_down_piece]:
                distance[move_down_piece] = new_distance
                heappush(priority_queue, (new_distance, move_down_piece, move + ['drop']))
        else:
            add_move(board, generated_moves, current_piece, move, board_width)


        move_left_piece: Optional[PieceData] = move_left(board, current_piece, board_width)
        if move_left_piece is not None:
            new_distance = current_distance + 1
            if move_left_piece not in distance or new_distance < distance[move_left_piece]:
                distance[move_left_piece] = new_distance
                heappush(priority_queue, (new_distance, move_left_piece, move + ['move_left']))

        move_right_piece: Optional[PieceData] = move_right(board, current_piece, board_width)
        if move_right_piece is not None:
            new_distance = current_distance + 1
            if move_right_piece not in distance or new_distance < distance[move_right_piece]:
                distance[move_right_piece] = new_distance
                heappush(priority_queue, (new_distance, move_right_piece, move + ['move_right']))

        rotate_cw_piece: Optional[PieceData] = rotate_cw(board, current_piece, board_width)
        if rotate_cw_piece is not None:
            new_distance = current_distance + 1
            if rotate_cw_piece not in distance or new_distance < distance[rotate_cw_piece]:
                distance[rotate_cw_piece] = new_distance
                heappush(priority_queue, (new_distance, rotate_cw_piece, move + ['rotate_cw']))

        rotate_ccw_piece: Optional[PieceData] = rotate_ccw(board, current_piece, board_width)
        if rotate_ccw_piece is not None:
            new_distance = current_distance + 1
            if rotate_ccw_piece not in distance or new_distance < distance[rotate_ccw_piece]:
                distance[rotate_ccw_piece] = new_distance
                heappush(priority_queue, (new_distance, rotate_ccw_piece, move + ['rotate_ccw']))


def short_dijkstra_generate_move_helper(board: Board, current_piece: PieceData, generated_moves: Dict[PieceData, Move], board_height: int, board_width: int, held: bool=False):
    priority_queue: List[Tuple[int, PieceData, Move]] = [(0, current_piece, ['hold'] if held else [])]
    visited: Set[PieceData] = set()
    distance: Dict[PieceData, int] = {current_piece: 0}

    while priority_queue:
        current_distance, current_piece, move = heappop(priority_queue)

        if current_piece in visited:
            continue

        visited.add(current_piece)
        add_move(board, generated_moves, current_piece, move, board_width)

        move_down_piece: Optional[PieceData] = move_down(board, current_piece, board_width)
        if move_down_piece is not None:
            new_distance = current_distance + 1
            if move_down_piece not in distance or new_distance < distance[move_down_piece]:
                distance[move_down_piece] = new_distance
                heappush(priority_queue, (new_distance, move_down_piece, move + ['drop']))

            sonic_down_piece: PieceData = sonic_drop(board, current_piece, board_width)
            if sonic_down_piece is not None:
                new_distance = current_distance + 1
                if sonic_down_piece not in distance or new_distance < distance[sonic_down_piece]:
                    distance[sonic_down_piece] = new_distance
                    heappush(priority_queue, (new_distance, sonic_down_piece, move + ['sonic_drop']))

        move_left_piece: Optional[PieceData] = move_left(board, current_piece, board_width)
        if move_left_piece is not None:
            new_distance = current_distance + 1
            if move_left_piece not in distance or new_distance < distance[move_left_piece]:
                distance[move_left_piece] = new_distance
                heappush(priority_queue, (new_distance, move_left_piece, move + ['move_left']))

            sonic_left_piece: PieceData = sonic_left(board, current_piece, board_width)
            if sonic_left_piece is not None:
                new_distance = current_distance + 1
                if sonic_left_piece not in distance or new_distance < distance[sonic_left_piece]:
                    distance[sonic_left_piece] = new_distance
                    heappush(priority_queue, (new_distance, sonic_left_piece, move + ['sonic_left']))

        move_right_piece: Optional[PieceData] = move_right(board, current_piece, board_width)
        if move_right_piece is not None:
            new_distance = current_distance + 1
            if move_right_piece not in distance or new_distance < distance[move_right_piece]:
                distance[move_right_piece] = new_distance
                heappush(priority_queue, (new_distance, move_right_piece, move + ['move_right']))

            sonic_right_piece: PieceData = sonic_right(board, current_piece, board_width)
            if sonic_right_piece is not None:
                new_distance = current_distance + 1
                if sonic_right_piece not in distance or new_distance < distance[sonic_right_piece]:
                    distance[sonic_right_piece] = new_distance
                    heappush(priority_queue, (new_distance, sonic_right_piece, move + ['sonic_right']))

        rotate_cw_piece: Optional[PieceData] = rotate_cw(board, current_piece, board_width)
        if rotate_cw_piece is not None:
            new_distance = current_distance + 1
            if rotate_cw_piece not in distance or new_distance < distance[rotate_cw_piece]:
                distance[rotate_cw_piece] = new_distance
                heappush(priority_queue, (new_distance, rotate_cw_piece, move + ['rotate_cw']))

        rotate_ccw_piece: Optional[PieceData] = rotate_ccw(board, current_piece, board_width)
        if rotate_ccw_piece is not None:
            new_distance = current_distance + 1
            if rotate_ccw_piece not in distance or new_distance < distance[rotate_ccw_piece]:
                distance[rotate_ccw_piece] = new_distance
                heappush(priority_queue, (new_distance, rotate_ccw_piece, move + ['rotate_ccw']))
