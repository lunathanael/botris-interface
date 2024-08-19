import copy
import math
import random
from typing import Deque, Dict, List, Literal, Optional, Tuple

from botris.interface.models import PublicGarbageLine as PublicGarbageLine

from .models import (
    AttackTable,
    Block,
    Board,
    ClearName,
    GarbageLine,
    Piece,
    PieceData,
    ScoreData,
    ScoreInfo,
)
from .pieces import (
    I_WALLKICKS,
    WALLKICKS,
    PieceMatrix,
    get_piece_border,
    get_piece_mask,
    get_piece_matrix,
)


def get_subgrid_mask(
    board: Board, start_x: int, start_y: int, board_width: int, board_height: int
) -> int:
    x_max = min(start_x + 4, board_width)
    y_min = max(start_y - 3, 0)
    y_max = min(start_y + 1, board_height)

    subgrid_mask: int = 0

    for y in range(y_min, y_max):
        for x in range(start_x, x_max):
            if board[y][x]:
                subgrid_mask += 1 << ((y - (start_y - 3)) * 4 + x - start_x)

    return subgrid_mask


def check_collision(board: Board, piece_data: PieceData, board_width: int) -> bool:
    return _check_collision(
        board,
        piece_data.piece,
        piece_data.x,
        piece_data.y,
        piece_data.rotation,
        board_width,
    )


def _check_collision(
    board: Board,
    piece: Piece,
    piece_x: int,
    piece_y: int,
    piece_rotation: Literal[0, 1, 2, 3],
    board_width: int,
) -> bool:
    lowest_x, highest_x, lowest_y, highest_y = get_piece_border(piece, piece_rotation)
    if (
        ((piece_x + lowest_x) < 0)
        or ((piece_x + highest_x) >= board_width)
        or ((piece_y - highest_y) < 0)
    ):
        return True

    board_height: int = len(board)
    if piece_y - 3 >= board_height:
        return False

    board_mask = get_subgrid_mask(board, piece_x, piece_y, board_width, board_height)
    piece_mask = get_piece_mask(piece, piece_rotation)

    if piece_mask & board_mask:
        return True
    return False


def check_immobile(board: Board, piece_data: PieceData, board_width: int) -> bool:
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        new_piece_data: PieceData = PieceData(
            piece_data.piece, piece_data.x + dx, piece_data.y + dy, piece_data.rotation
        )
        if not check_collision(board, new_piece_data, board_width):
            return False
    return True


def _place_piece(board: Board, piece_data: PieceData, board_width: int) -> Board:
    piece_matrix: PieceMatrix = get_piece_matrix(piece_data.piece, piece_data.rotation)
    for piece_y, row in enumerate(piece_matrix):
        for piece_x, cell in enumerate(row):
            if cell:
                board_x: int = piece_data.x + piece_x
                board_y: int = piece_data.y - piece_y
                if board_y >= len(board):
                    diff: int = board_y - len(board) + 1
                    board.extend([[None] * board_width for _ in range(diff)])
                board[board_y][board_x] = cell
    return board


def place_piece(board: Board, piece_data: PieceData, board_width: int) -> Board:
    new_board: Board = [row.copy() for row in board]
    _place_piece(new_board, piece_data, board_width)
    return new_board


def clear_lines(board: Board) -> Tuple[Board, List[Dict[str, int | List[Block]]]]:
    new_board: Board = [
        row for row in board if not all(cell is not None for cell in row)
    ]
    cleared_lines: List[Dict[str, int | List[Block]]] = [
        {"height": i, "blocks": row}
        for i, row in enumerate(board)
        if all(cell is not None for cell in row)
    ]
    return new_board, cleared_lines


def check_pc(board) -> bool:
    return len(board) == 0 or all(all(cell is None for cell in row) for row in board)


def calculate_score(
    score_info: ScoreInfo, attack_table: AttackTable, combo_table: List[int]
) -> ScoreData:
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
        return ScoreData(score=0, b2b=b2b, combo=0, clear_name=None, all_spin=False)

    new_combo: int = combo + 1

    if is_immobile:
        all_spin = True
        is_b2b_clear = True
        match lines_cleared:
            case 1:
                score += attack_table.ass
                clear_name = "All-Spin Single"
            case 2:
                score += attack_table.asd
                clear_name = "All-Spin Double"
            case 3:
                score += attack_table.ast
                clear_name = "All-Spin Triple"
    else:
        match lines_cleared:
            case 1:
                score += attack_table.single
                clear_name = "Single"
                is_b2b_clear = False
            case 2:
                score += attack_table.double
                clear_name = "Double"
                is_b2b_clear = False
            case 3:
                score += attack_table.triple
                clear_name = "Triple"
                is_b2b_clear = False
            case 4:
                score += attack_table.quad
                clear_name = "Quad"
                is_b2b_clear = True

    if b2b and is_b2b_clear:
        score += attack_table.b2b

    if new_combo > 0:
        combo_index = min(new_combo - 1, len(combo_table) - 1)
        score += combo_table[combo_index]

    if pc:
        score = attack_table.pc
        clear_name = "Perfect Clear"

    return ScoreData(
        score=score,
        b2b=is_b2b_clear,
        combo=new_combo,
        clear_name=clear_name,
        all_spin=all_spin,
    )


def generate_garbage(
    garbage_queue: List[PublicGarbageLine], garbage_messiness: float, board_width: int
) -> List[GarbageLine]:
    garbage: List[GarbageLine] = []
    hole_index: Optional[int] = None

    for garbage_line in garbage_queue:
        if hole_index is None or random.random() < garbage_messiness:
            hole_index = math.floor(random.random() * board_width)
        garbage.append(GarbageLine(delay=garbage_line.delay, index=hole_index))

    return garbage


def process_garbage(
    board: Board, garbage_queue: Deque[PublicGarbageLine], board_width: int
) -> Tuple[Board, List[int]]:
    expired_indices: List[int] = []

    garbage_length: int = len(garbage_queue)
    for _ in range(garbage_length):
        garbage_line: PublicGarbageLine = garbage_queue.popleft()
        if garbage_line.delay <= 0:
            expired_indices.append(garbage_line.index)
            continue
        garbage_line.delay -= 1
        garbage_queue.append(garbage_line)

    board = _add_garbage(board, expired_indices, board_width)
    return board, expired_indices


def _add_garbage(board: Board, garbage_indices: List[int], board_width: int) -> Board:
    lines: List[List[Block]] = []
    for hold_index in reversed(garbage_indices):
        line: List[Block] = ["G"] * board_width
        line[hold_index] = None
        lines.append(line)

    return lines + board


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
    return variance**0.5


def create_piece(piece: Piece, board_height: int, board_width: int) -> PieceData:
    x: int = board_width // 2 - ((len(get_piece_matrix(piece, 0)[0]) + 1) // 2)
    y: int = board_height
    return PieceData(piece=piece, x=x, y=y, rotation=0)


def move_left(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    if _check_collision(
        board, piece.piece, piece.x - 1, piece.y, piece.rotation, board_width
    ):
        return None
    return PieceData(piece.piece, piece.x - 1, piece.y, piece.rotation)


def move_right(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    if _check_collision(
        board, piece.piece, piece.x + 1, piece.y, piece.rotation, board_width
    ):
        return None
    return PieceData(piece.piece, piece.x + 1, piece.y, piece.rotation)


def move_drop(board: Board, piece: PieceData, board_width: int) -> Optional[PieceData]:
    if _check_collision(
        board, piece.piece, piece.x, piece.y - 1, piece.rotation, board_width
    ):
        return None
    return PieceData(piece.piece, piece.x, piece.y - 1, piece.rotation)


def sonic_drop(board: Board, piece: PieceData, board_width: int) -> PieceData:
    drop_dist: int = 1
    while True:
        if _check_collision(
            board,
            piece.piece,
            piece.x,
            piece.y - drop_dist,
            piece.rotation,
            board_width,
        ):
            return PieceData(
                piece.piece, piece.x, piece.y - drop_dist + 1, piece.rotation
            )
        drop_dist += 1


def sonic_left(board: Board, piece: PieceData, board_width: int) -> PieceData:
    left_dist: int = 1
    while True:
        if _check_collision(
            board,
            piece.piece,
            piece.x - left_dist,
            piece.y,
            piece.rotation,
            board_width,
        ):
            return PieceData(
                piece.piece, piece.x - left_dist + 1, piece.y, piece.rotation
            )
        left_dist += 1


def sonic_right(board: Board, piece: PieceData, board_width: int) -> PieceData:
    right_dist: int = 1
    while True:
        if _check_collision(
            board,
            piece.piece,
            piece.x + right_dist,
            piece.y,
            piece.rotation,
            board_width,
        ):
            return PieceData(
                piece.piece, piece.x + right_dist - 1, piece.y, piece.rotation
            )
        right_dist += 1


def rotate_cw(
    board: Board, current: PieceData, board_width: int
) -> Optional[PieceData]:
    initial_rotation: Literal[0, 1, 2, 3] = current.rotation
    new_rotation: Literal[0, 1, 2, 3] = (initial_rotation + 1) % 4

    wallkicks = I_WALLKICKS if current.piece == Piece.I else WALLKICKS
    kick_data = wallkicks[initial_rotation][new_rotation]

    for dx, dy in kick_data:
        if not _check_collision(
            board,
            current.piece,
            current.x + dx,
            current.y + dy,
            new_rotation,
            board_width,
        ):
            return PieceData(
                current.piece, current.x + dx, current.y + dy, new_rotation
            )

    return None


def rotate_ccw(
    board: Board, current: PieceData, board_width: int
) -> Optional[PieceData]:
    initial_rotation: Literal[0, 1, 2, 3] = current.rotation
    new_rotation: Literal[0, 1, 2, 3] = (initial_rotation + 3) % 4

    wallkicks = I_WALLKICKS if current.piece == Piece.I else WALLKICKS
    kick_data = wallkicks[initial_rotation][new_rotation]

    for dx, dy in kick_data:
        if not _check_collision(
            board,
            current.piece,
            current.x + dx,
            current.y + dy,
            new_rotation,
            board_width,
        ):
            return PieceData(
                current.piece, current.x + dx, current.y + dy, new_rotation
            )

    return None


def get_board_hole_count(board: Board, board_width: int) -> int:
    """
    Calculate the number of holes in the given game board.

    Parameters:
    ----------
    board : Board
        The game board represented as a 2D list.
    board_width : int
        The width of the game board.

    Returns:
    ----------
    int:
    The number of holes in the game board.
    """
    hole_count: int = 0
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                if (
                    (i == 0 or board[i - 1][j] is not None)
                    and (j == 0 or board[i][j - 1] is not None)
                    and (j == board_width - 1 or board[i][j + 1] is not None)
                    and (i == len(board) - 1 or board[i + 1][j] is not None)
                ):
                    hole_count += 1
    return hole_count


def get_board_ledge_count(board: Board) -> int:
    """
    Calculate the number of ledges in the given game board.

    Parameters:
    ----------
    board : Board
        The game board represented as a 2D list.

    Returns:
    ----------
    int:
        The number of ledges in the game board.
    """
    ledge_count: int = 0

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                if i != len(board) - 1 and board[i + 1][j] is not None:
                    ledge_count += 1
    return ledge_count


def get_board_hole_and_ledge_count(board: Board, board_width: int) -> Tuple[int, int]:
    """
    Calculate the number of holes and ledges in the given game board.

    Parameters:
    ----------
    board : Board
        The game board represented as a 2D list.
    board_width : int
        The width of the game board.

    Returns:
    ----------
    Tuple[int, int]:
        The number of holes and ledges in the game board.
    """
    hole_count: int = 0
    ledge_count: int = 0
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                if (
                    (i == 0 or board[i - 1][j] is not None)
                    and (j == 0 or board[i][j - 1] is not None)
                    and (j == board_width - 1 or board[i][j + 1] is not None)
                    and (i == len(board) - 1 or board[i + 1][j] is not None)
                ):
                    hole_count += 1
                elif i != len(board) - 1 and board[i + 1][j] is not None:
                    ledge_count += 1
    return hole_count, ledge_count
