from typing import Optional, List

from .models import Board, Piece, PieceData, Command
from .utils import check_collision, check_immobile, create_piece

Move = List[Command]

def generate_moves(board: Board, piece: Piece, held: Optional[Piece]):
    board_height: int = len(board)
    board_width: int = len(board[0])

    generated_moves: List[]

    current_piece: PieceData = create_piece(piece, board_height, board_width)
    if held is not None:
        held_piece: Optional[PieceData] = create_piece(held, board_height, board_width) if held else None