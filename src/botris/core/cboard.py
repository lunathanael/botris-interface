from __future__ import annotations

from typing import TYPE_CHECKING

from botris._core import Board

from .cpiece import CPiece


class CBoard:
    """
    A Python interface for the C++ Board class, where each method calls the corresponding
    method in the base class.

    Attributes:
    -----------
    width : int (size_t)
        The width of the board.
    visual_height : int (size_t)
        The visual height of the board.
    height : int (size_t)
        The height of the board.
    board : List[int] (array<u32, CBoard.width>)
        The board data. A 1D list of integers representing the board.

    Methods:
    --------
    __init__(self)
        Initialize the board.
    get(self, x: int, y: int) -> int (u32)
        Get the value at a specific coordinate on the board.
    get_column(self, x: int) -> int (u32)
        Get the value of a specific column on the board.
    set(self, x: int, y: int) -> None
        Set the value at a specific coordinate on the board.
    set(self, piece: CPiece) -> None
        Set the piece on the board.
    unset(self, x: int, y: int) -> None
        Unset the value at a specific coordinate on the board.
    clearLines(self) -> int
        Clear any full lines on the board.
    filledRows(self) -> int
        Get the number of filled rows on the board.
    is_empty(self) -> bool
        Check if the board is empty.
    bounded(self, height: int) -> int (u32)
        Returns something, this is used with NANA.
    not_empty(self, height: int) -> int (u32)
        Get the number of non-empty rows on the board.
    full(self, height: int) -> int (u32)
        Get the number of rows that are matching the height.
    has_imbalanced_split(self, height: int) -> bool
        Check if the board has an imbalanced split.
    empty_cells(self, height: int) -> int (u32)
        Get the number of empty cells on the board.
    is_convex(self) -> bool
        Check if the board is convex.
    get_garbage_height(self) -> int
        Get the height of the garbage on the board.
    is_low(self) -> bool
        Check if the board is low.
    copy(self) -> CBoard
        Copy the board.
    """

    width: int = Board.width
    visual_height: int = Board.visual_height
    height: int = Board.height

    @property
    def board(self) -> list[int]:
        """
        Get the board data.

        Note that when setting the board data, indexing is not allowed.
        Instead, the entire board data must be set at once.

        Returns:
        --------
        List[int] (array<u32, CBoard.width>)
            The board data.
        """
        pass

    @board.setter
    def board(self, value: list[int]) -> None:
        """
        Set the board data.

        Parameters:
        -----------
        value : List[int] (array<u32, CBoard.width>)
            The board data.
        """
        pass

    def __init__(self):
        """
        Initialize the board by calling the base class constructor.
        This will fill the board with zeros.

        """
        pass

    def get(self, x: int, y: int) -> int:
        """
        Get the value at a specific coordinate on the board.

        Parameters:
        -----------
        x : int (size_t)
            The x-coordinate.
        y : int (size_t)
            The y-coordinate.

        Returns:
        --------
        int
            The value at the specified location.
        """
        pass

    def get_column(self, x: int) -> int:
        """
        Get the value of a specific column on the board.

        Parameters:
        -----------
        x : int (size_t)
            The x-coordinate.

        Returns:
        --------
        int (u32)
            The value of the specified column.
        """
        pass

    def set(self, x: int, y: int) -> None:
        """
        Set the value at a specific coordinate on the board.

        Parameters:
        -----------
        x : int (size_t)
            The x-coordinate.
        y : int (size_t)
            The y-coordinate.
        """
        pass

    def set(self, piece: CPiece) -> None:
        """
        Set the piece on the board.

        Parameters:
        -----------
        piece : Piece
            The piece to set.
        """
        pass

    def unset(self, x: int, y: int) -> None:
        """
        Unset the value at a specific coordinate on the board.

        Parameters:
        -----------
        x : int (size_t)
            The x-coordinate.
        y : int (size_t)
            The y-coordinate.
        """
        pass

    def clearLines(self) -> int:
        """
        Clear any full lines on the board.

        Returns:
        --------
        int
            The number of lines cleared.
        """
        pass

    def filledRows(self) -> int:
        """
        Get the number of filled rows on the board.

        Returns:
        --------
        int
            The number of filled rows.
        """
        pass

    def is_empty(self) -> bool:
        """
        Check if the board is empty.

        Returns:
        --------
        bool
            True if the board is empty, False otherwise.
        """
        pass

    def bounded(self, height: int) -> int:
        """
        Returns something, this is used with NANA.
        TODO: Figure out what this does.

        Parameters:
        -----------
        height : int
            The height to bound.

        Returns:
        --------
        int (u32)
            Something about the bounded board
        """
        pass

    def not_empty(self, height: int) -> int:
        """
        Get the number of non-empty rows on the board.
        TODO: Remove height as it is not used.

        Parameters:
        -----------
        height : int
            The height to check.

        Returns:
        --------
        int (u32)
            A mask of non-empty rows.
        """

    def full(self, height: int) -> int:
        """
        Get the number of rows that are matching the height.

        Parameters:
        -----------
        height : int
            The height to check.

        Returns:
        --------
        int (u32)
            A mask of full rows.
        """
        pass

    def has_imbalanced_split(self, height: int) -> bool:
        """
        Check if the board has an imbalanced split.

        Parameters:
        -----------
        height : int
            The height to check.

        Returns:
        --------
        bool
            True if the board has an imbalanced split, False otherwise.
        """
        pass

    def empty_cells(self, height: int) -> int:
        """
        Get the number of empty cells on the board.

        Parameters:
        -----------
        height : int
            The height to check.

        Returns:
        --------
        int (u32)
            The number of empty cells.
        """
        pass

    def is_convex(self) -> bool:
        """
        Check if the board is convex.

        Returns:
        --------
        bool
            True if the board is convex, False otherwise.
        """
        pass

    def get_garbage_height(self) -> int:
        """
        Get the height of the garbage on the board.

        Returns:
        --------
        int
            The height of the garbage.
        """
        pass

    def is_low(self) -> bool:
        """
        Check if the board is low.

        Returns:
        --------
        bool
            True if the board is low, False otherwise.
        """
        pass

    def copy(self) -> CBoard:
        """
        Copy the board.

        Returns:
        --------
        CBoard
            A copy of the board.
        """
        pass


if not TYPE_CHECKING:
    CBoard = Board

__all__ = ["CBoard"]
