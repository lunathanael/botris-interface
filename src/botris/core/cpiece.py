from __future__ import annotations

from typing import TYPE_CHECKING

from .cconstants import CCoord, CPieceType, CRotateDirection, CspinType, CTurnDirection


class CPiece:
    """
    A Python interface for the C++ Piece class, where each method calls the corresponding
    method in the base class.

    Attributes:
    -----------
    minos : List[CCoord]
        The minos of the piece.
    position : CCoord
        The position of the piece.
    rotation : CRotateDirection
        The rotation of the piece.
    type : CPieceType
        The type of the piece.
    spin : CspinType
        The spin type of the piece.

    Methods:
    --------
    __init__(self, type: CPieceType)
        Initialize the piece.
    __init__(self, type: CPieceType, dir: CRotateDirection)
        Initialize the piece.
    __init__(self, type: CPieceType, dir: CRotateDirection, pos: CCoord)
        Initialize the piece.
    __init__(self, type: CPieceType, dir: CRotateDirection, pos: CCoord, spn: CspinType)
        Initialize the piece.
    rotate(direction: CTurnDirection) -> None
        Rotate the piece.
    calculate_rotate(direction: CTurnDirection) -> None
        Calculate the rotation of the piece.
    hash() -> int (u32)
        Get the hash of the piece.
    compact_hash() -> int (u32)
        Get the compact hash of the piece.
    copy() -> CPiece
        Get a copy of the piece.
    """

    @property
    def minos(self) -> list[CCoord]:
        """
        Get the minos of the piece.

        Note that when setting the minos data, indexing is not allowed.
        Instead, the entire minos data must be set at once.

        Returns:
        --------
        List[CCoord]
            The minos of the piece.
        """
        pass

    @minos.setter
    def minos(self, value: list[CCoord]) -> None:
        """
        Set the minos of the piece.

        Parameters:
        -----------
        value : List[CCoord]
            The minos of the piece.
        """
        pass

    @property
    def position(self) -> CCoord:
        """
        Get the position of the piece.

        Returns:
        --------
        CCoord
            The position of the piece.
        """
        pass

    @position.setter
    def position(self, value: CCoord) -> None:
        """
        Set the position of the piece.

        Parameters:
        -----------
        value : CCoord
            The position of the piece.
        """
        pass

    @property
    def rotation(self) -> CRotateDirection:
        """
        Get the rotation of the piece.

        Returns:
        --------
        CRotateDirection
            The rotation of the piece.
        """
        pass

    @rotation.setter
    def rotation(self, value: CRotateDirection) -> None:
        """
        Set the rotation of the piece.

        Parameters:
        -----------
        value : CRotateDirection
            The rotation of the piece.
        """
        pass

    @property
    def type(self) -> CPieceType:
        """
        Get the type of the piece.

        Returns:
        --------
        CPieceType
            The type of the piece.
        """
        pass

    @type.setter
    def type(self, value: CPieceType) -> None:
        """
        Set the type of the piece.

        Parameters:
        -----------
        value : CPieceType
            The type of the piece.
        """
        pass

    @property
    def spin(self) -> CspinType:
        """
        Get the spin type of the piece.

        Returns:
        --------
        CspinType
            The spin type of the piece.
        """
        pass

    @spin.setter
    def spin(self, value: CspinType) -> None:
        """
        Set the spin type of the piece.

        Parameters:
        -----------
        value : CspinType
            The spin type of the piece.
        """
        pass

    def __init__(self, type: CPieceType):
        """
        Initialize the piece.

        Parameters:
        -----------
        type : CPieceType
            The type of the piece.
        """
        pass

    def __init__(self, type: CPieceType, dir: CRotateDirection):
        """
        Initialize the piece.

        Parameters:
        -----------
        type : CPieceType
            The type of the piece.
        dir : CRotateDirection
            The direction of the piece.
        """
        pass

    def __init__(self, type: CPieceType, dir: CRotateDirection, pos: CCoord):
        """
        Initialize the piece.

        Parameters:
        -----------
        type : CPieceType
            The type of the piece.
        dir : CRotateDirection
            The direction of the piece.
        pos : CCoord
            The position of the piece.
        """
        pass

    def __init__(
        self, type: CPieceType, dir: CRotateDirection, pos: CCoord, spn: CspinType
    ):
        """
        Initialize the piece.

        Parameters:
        -----------
        type : CPieceType
            The type of the piece.
        dir : CRotateDirection
            The direction of the piece.
        pos : CCoord
            The position of the piece.
        spn : CspinType
            The spin type of the piece.
        """
        pass

    def rotate(self, direction: CTurnDirection) -> None:
        """
        Lookup the rotate the piece.

        Parameters:
        -----------
        direction : CTurnDirection
            The direction to rotate the piece.
        """
        pass

    def calculate_rotate(self, direction: CTurnDirection) -> None:
        """
        Calculate the rotation of the piece.

        Parameters:
        -----------
        direction : CTurnDirection
            The direction to rotate the piece.
        """
        pass

    def hash(self) -> int:
        """
        Get the hash of the piece.

        Returns:
        --------
        int (u32)
            The hash of the piece.
        """
        pass

    def compact_hash(self) -> int:
        """
        Get the compact hash of the piece.

        Returns:
        --------
        int (u32)
            The compact hash of the piece.
        """
        pass

    def copy(self) -> CPiece:
        """
        Get a copy of the piece.

        Returns:
        --------
        CPiece
            A copy of the piece.
        """
        pass


if not TYPE_CHECKING:
    from botris._core import Piece

    CPiece = Piece

__all__ = [
    "CPiece",
]
