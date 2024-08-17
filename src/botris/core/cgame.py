from __future__ import annotations

from typing import List, Optional

from botris._core import Game, Piece, Board, Botris
from botris._core.constants import spinType, Movement, PieceType

class CGame(Game):
    """
    A Python wrapper for the C++ Game class, where each method calls the corresponding 
    method in the base class.
    """

    def __init__(self):
        """Initialize the game by calling the base class constructor."""
        super().__init__()

    def place_piece(self) -> None:
        """Place the current piece on the board."""
        super().place_piece()

    def place_piece(self, piece: Piece) -> bool:
        """
        Place a specified piece on the board.

        Parameters:
        -----------
        piece : Piece
            The piece to be placed.

        Returns:
        --------
        bool
            True if it's the first hold, False otherwise.
        """
        return super().place_piece(piece)

    def do_hold(self) -> None:
        """Perform a hold action, swapping the current piece with the held piece."""
        super().do_hold()

    def add_garbage(self, lines: int, location: int) -> None:
        """
        Add garbage lines to the board.

        Parameters:
        -----------
        lines : int
            The number of lines to add.
        location : int
            The column where the hole in the garbage lines will be placed.
        """
        super().add_garbage(lines, location)

    def damage_sent(self, linesCleared: int, spinType: spinType, pc: bool) -> int:
        """
        Calculate the damage sent based on lines cleared and spin type.

        Parameters:
        -----------
        linesCleared : int
            The number of lines cleared.
        spinType : spinType
            The type of spin used.
        pc : bool
            Whether a perfect clear was achieved.

        Returns:
        --------
        int
            The damage to be sent to the opponent.
        """
        return super().damage_sent(linesCleared, spinType, pc)

    def process_movement(self, piece: Piece, movement: Movement) -> None:
        """
        Process the movement of a piece.

        Parameters:
        -----------
        piece : Piece
            The piece to be moved.
        movement : Movement
            The movement to apply to the piece.
        """
        super().process_movement(piece, movement)

    def get_possible_piece_placements(self) -> List[Piece]:
        """
        Get all possible placements for the current piece.

        Returns:
        --------
        List[Piece]
            A list of all valid piece placements.
        """
        return super().get_possible_piece_placements()

    @property
    def board(self) -> Board:
        """Get or set the current game board."""
        return super().board

    @board.setter
    def board(self, value: Board) -> None:
        super().board.set(self, value)

    @property
    def current_piece(self) -> Piece:
        """Get or set the current piece."""
        return super().current_piece

    @current_piece.setter
    def current_piece(self, value: Piece) -> None:
        super().current_piece.set(self, value)

    @property
    def hold(self) -> Optional[PieceType]:
        """Get or set the held piece."""
        return super().hold

    @hold.setter
    def hold(self, value: Optional[PieceType]) -> None:
        super().hold.set(self, value)

    @property
    def garbage_meter(self) -> int:
        """Get or set the garbage meter."""
        return super().garbage_meter

    @garbage_meter.setter
    def garbage_meter(self, value: int) -> None:
        super().garbage_meter.set(self, value)

    @property
    def b2b(self) -> int:
        """Get or set the back-to-back counter."""
        return super().b2b

    @b2b.setter
    def b2b(self, value: int) -> None:
        super(CGame, CGame).b2b.__set__(self, value)

    @property
    def combo(self) -> int:
        """Get or set the combo counter."""
        return super().combo

    @combo.setter
    def combo(self, value: int) -> None:
        super().combo.set(self, value)

    @property
    def queue(self) -> List[PieceType]:
        """Get or set the piece queue."""
        return super().queue

    @queue.setter
    def queue(self, value: List[PieceType]) -> None:
        super().queue.set(self, value)

    @property
    def mode(self) -> Botris:
        """Get or set the current game mode."""
        return super().mode

    @mode.setter
    def mode(self, value: Botris) -> None:
        super().mode.set(self, value)

    def copy(self) -> CGame:
        """
        Create a copy of the game state.

        Returns:
        --------
        Game
            A new instance of the game with the same state as the current game.
        """
        return super().copy()