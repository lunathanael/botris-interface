from botris.core import CGame, CBoard, CPiece
from botris.core.cconstants import CPieceType, CspinType
from .models import Board, Block, PieceData

def to_cboard(board: Board) -> CBoard:
    cboard: CBoard = CBoard()
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            cboard.set(x, y)
    return cboard

def to_board(cboard: CBoard) -> Board:
    board: Board = []
    for y in range(32):
        row: list[Block] = []
        for x in range(CBoard.width):
            if cboard.get(x, y):
                row.append("G")
            else:
                row.append(None)
        if any(row):
            board.append(row)
        else:
            break
    return board