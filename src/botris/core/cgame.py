from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from botris._core import Game

from .cboard import CBoard
from .cconstants import CMovement, CPieceType, CspinType
from .cmode import CBotris
from .cpiece import CPiece


class CGame:
    """
    A Python wrapper for the C++ Game class, where each method calls the corresponding
    method in the base class.

    Attributes:
    -----------
    QUEUE_SIZE : int
        The size of the queue.
    board : CBoard
        The board.
    current_piece : CPiece
        The current piece.
    hold : Optional[CPieceType]
        The held piece.
    garbage_meter : int (u8)
        The garbage meter.
    b2b : int (u16)
        The back-to-back counter.
    combo : int (u16)
        The combo counter.
    queue : List[CPieceType]
        The queue.
    mode : CBotris
        The Botris mode instance.

    Methods:
    --------
    __init__(self)
        Initialize the game.
    place_piece(self) -> None
        Place the current piece on the board.
    place_piece(self, piece: CPiece) -> bool
        Place a specified piece on the board.
    do_hold(self) -> None
        Perform a hold action, swapping the current piece with the held piece.
    add_garbage(self, lines: int, location: int) -> None
        Add garbage lines to the board.
    damage_sent(self, linesCleared: int, spinType: CspinType, pc: bool) -> int
        Calculate the damage sent based on lines cleared and spin type.
    process_movement(self, piece: CPiece, movement: CMovement) -> None
        Process the movement of a piece.
    get_possible_piece_placements(self) -> List[CPiece]
        Get all possible placements for the current piece.
    copy(self) -> CGame
        Create a copy of the game state
    """

    QUEUE_SIZE: int = Game.QUEUE_SIZE

    @property
    def board(self) -> CBoard:
        """
        Get or set the board.

        Returns:
        --------
        Board
            The board.
        """
        pass

    @board.setter
    def board(self, value: CBoard) -> None:
        """
        Set the board.

        Parameters:
        -----------
        value : Board
            The board.
        """
        pass

    @property
    def current_piece(self) -> CPiece:
        """
        Get or set the current piece.

        Returns:
        --------
        CPiece
            The current piece.
        """
        pass

    @current_piece.setter
    def current_piece(self, value: CPiece) -> None:
        """
        Set the current piece.

        Parameters:
        -----------
        value : CPiece
            The current piece.
        """
        pass

    @property
    def hold(self) -> Optional[CPieceType]:
        """
        Get or set the held piece.

        Returns:
        --------
        Optional[CPieceType]
            The held piece.
        """
        pass

    @hold.setter
    def hold(self, value: CPieceType) -> None:
        """
        Set the held piece.

        Parameters:
        -----------
        value : CPieceType
            The piece to be held.
        """
        pass

    @property
    def garbage_meter(self) -> int:
        """
        Get or set the garbage meter.

        Returns:
        --------
        int (u8)
            The garbage meter.
        """
        pass

    @garbage_meter.setter
    def garbage_meter(self, value: int) -> None:
        """
        Set the garbage meter.

        Parameters:
        -----------
        value : int (u8)
            The garbage meter.
        """
        pass

    @property
    def b2b(self) -> int:
        """
        Get or set the back-to-back counter.

        Returns:
        --------
        int (u16)
            The back-to-back counter.
        """
        pass

    @b2b.setter
    def b2b(self, value: int) -> None:
        """
        Set the back-to-back counter.

        Parameters:
        -----------
        value : int (u16)
            The back-to-back counter.
        """
        pass

    @property
    def combo(self) -> int:
        """
        Get or set the combo counter.

        Returns:
        --------
        int (u16)
            The combo counter.
        """
        pass

    @combo.setter
    def combo(self, value: int) -> None:
        """
        Set the combo counter.

        Parameters:
        -----------
        value : int (u16)
            The combo counter.
        """
        pass

    @property
    def queue(self) -> list[CPieceType]:
        """
        Get or set the queue.

        Note that when setting the queue data, indexing is not allowed.
        Instead, the entire queue data must be set at once.

        Returns:
        --------
        List[CPieceType]
            The queue.
        """
        pass

    @queue.setter
    def queue(self, value: list[CPieceType]) -> None:
        """
        Set the queue.

        Parameters:
        -----------
        value : List[CPieceType]
            The queue.
        """
        pass

    @property
    def mode(self) -> CBotris:
        """
        Get the Botris Mode instance.

        Returns:
        --------
        Botris
            The Botris instance.
        """
        pass

    @mode.setter
    def mode(self, value: CBotris) -> None:
        """
        Set the Botris Mode instance.

        Parameters:
        -----------
        value : Botris
            The Botris instance.
        """
        pass

    def __init__(self):
        """
        Initialize the game.
        """
        pass

    def place_piece(self) -> None:
        """
        Place the current piece on the board.
        """
        pass

    def place_piece(self, piece: CPiece) -> bool:
        """
        Place a specified piece on the board.

        Parameters:
        -----------
        piece : CPiece
            The piece to be placed.

        Returns:
        --------
        bool
            True if it's the first hold, False otherwise.
        """
        pass

    def do_hold(self) -> None:
        """
        Perform a hold action, swapping the current piece with the held piece.
        """
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

    def damage_sent(self, linesCleared: int, spinType: CspinType, pc: bool) -> int:
        """
        Calculate the damage sent based on lines cleared and spin type.

        Parameters:
        -----------
        linesCleared : int
            The number of lines cleared.
        spinType : CspinType
            The type of spin used.
        pc : bool
            Whether a perfect clear was achieved.

        Returns:
        --------
        int
            The damage to be sent to the opponent.
        """
        pass

    def process_movement(self, piece: CPiece, movement: CMovement) -> None:
        """
        Process the movement of a piece.

        Parameters:
        -----------
        piece : CPiece
            The piece to be moved.
        movement : CMovement
            The movement to apply to the piece.
        """
        pass

    def get_possible_piece_placements(self) -> list[CPiece]:
        """
        Get all possible placements for the current piece.

        Returns:
        --------
        List[Piece]
            A list of all valid piece placements. This is actually of type `VectorPiece`,
            although implementation is similar to `List[Piece]`.
        """
        pass

    def copy(self) -> CGame:
        """
        Create a copy of the game state.

        Returns:
        --------
        CGame
            A new instance of the game with the same state as the current game.
        """
        pass


if not TYPE_CHECKING:
    CGame = Game

__all__ = ["CGame"]
