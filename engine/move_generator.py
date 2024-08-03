from typing import Optional

from .models import Board, Piece, PieceData


def generate_moves(board: Board, piece: PieceData, held: Optional[Piece]):
