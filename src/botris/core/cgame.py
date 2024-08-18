from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from botris._core import Game, Piece, Board, Botris
from botris._core.constants import spinType, Movement, PieceType

class CGame:
    """
    A Python wrapper for the C++ Game class, where each method calls the corresponding 
    method in the base class.
    """

    def __init__(self):
        """Initialize the game by calling the base class constructor."""
        pass

    def place_piece(self) -> None:
        """Place the current piece on the board."""
        pass

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
        pass

    def do_hold(self) -> None:
        """Perform a hold action, swapping the current piece with the held piece."""
        pass

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
        pass

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
        pass

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
        pass

    def get_possible_piece_placements(self) -> List[Piece]:
        """
        Get all possible placements for the current piece.

        Returns:
        --------
        List[Piece]
            A list of all valid piece placements.
        """
        pass

    @property
    def board(self) -> Board:
        """Get or set the current game board."""
        pass

    @property
    def current_piece(self) -> Piece:
        """Get or set the current piece."""
        pass

    @property
    def hold(self) -> Optional[PieceType]:
        """Get or set the held piece."""
        pass

    @property
    def garbage_meter(self) -> int:
        """Get or set the garbage meter."""
        pass

    @property
    def b2b(self) -> int:
        """Get or set the back-to-back counter."""
        pass

    @property
    def combo(self) -> int:
        """Get or set the combo counter."""
        pass

    @property
    def queue(self) -> List[PieceType]:
        """Get or set the piece queue."""
        pass

    @property
    def mode(self) -> Botris:
        """Get or set the current game mode."""
        pass

    def copy(self) -> CGame:
        """
        Create a copy of the game state.

        Returns:
        --------
        Game
            A new instance of the game with the same state as the current game.
        """
        pass

if not TYPE_CHECKING:
    CGame = Game