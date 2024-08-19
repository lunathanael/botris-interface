from enum import IntEnum, auto
from typing import TYPE_CHECKING

from botris._core.constants import (
    n_minos,
    piece_definitions,
    piece_spawn_height,
    rot_piece_def,
)


class CspinType(IntEnum):
    """
    An enumeration of the spin types.
    """

    null = auto()
    mini = auto()
    normal = auto()


class CCoord:
    """
    An interface class representing a coordinate on the board.

    Attributes:
    -----------
    x : int (i8)
        The x-coordinate.
    y : int (i8)
        The y-coordinate.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize the coordinate.

        Parameters:
        -----------
        x : int (i8)
            The x-coordinate.
        y : int (i8)
            The y-coordinate.
        """
        pass

    @property
    def x(self) -> int:
        """
        Get the x-coordinate.

        Returns:
        --------
        int (i8)
            The x-coordinate.
        """
        pass

    @x.setter
    def x(self, value: int) -> None:
        """
        Set the x-coordinate.

        Parameters:
        -----------
        value : int (i8)
            The x-coordinate.
        """
        pass

    @property
    def y(self) -> int:
        """
        Get the y-coordinate.

        Returns:
        --------
        int (i8)
            The y-coordinate.
        """
        pass

    @y.setter
    def y(self, value: int) -> None:
        """
        Set the y-coordinate.

        Parameters:
        -----------
        value : int (i8)
            The y-coordinate.
        """
        pass


class CRotateDirection(IntEnum):
    """
    An enumeration of the rotation directions.
    """

    North = auto()
    East = auto()
    South = auto()
    West = auto()
    RotateDirections_N = auto()


class CColorType(IntEnum):
    """
    An enumeration of the color types of pieces.
    """

    S = auto()
    Z = auto()
    J = auto()
    L = auto()
    T = auto()
    O = auto()
    I = auto()

    Empty = auto()
    LineClear = auto()
    Garbage = auto()
    ColorTypes_N = auto()


class CPieceType(IntEnum):
    """
    An enumeration of the types of pieces.
    """

    S = CColorType.S
    Z = CColorType.Z
    J = CColorType.J
    L = CColorType.L
    T = CColorType.T
    O = CColorType.O
    I = CColorType.I

    Empty = CColorType.Empty
    PieceTypes_N = auto()


class CTurnDirection(IntEnum):
    """
    An enumeration of the turn directions.
    """

    Left = auto()
    Right = auto()


class CMovement(IntEnum):
    """
    An enumeration of the movement directions.
    """

    Left = auto()
    Right = auto()
    RotateClockwise = auto()
    RotateCounterClockwise = auto()
    SonicDrop = auto()


n_minos: int = n_minos
piece_definitions: list[list[CCoord]] = piece_definitions
rot_piece_def: list[list[list[CCoord]]] = rot_piece_def
piece_spawn_height: int = piece_spawn_height


if not TYPE_CHECKING:
    from botris._core.constants import (
        ColorType,
        Coord,
        Movement,
        PieceType,
        RotationDirection,
        TurnDirection,
        spinType,
    )

    CspinType = spinType
    CRotateDirection = RotationDirection
    CColorType = ColorType
    CPieceType = PieceType
    CTurnDirection = TurnDirection
    CMovement = Movement
    CCoord = Coord

__all__ = [
    "CspinType",
    "CRotateDirection",
    "CColorType",
    "CPieceType",
    "CTurnDirection",
    "CMovement",
    "CCoord",
    "n_minos",
    "piece_definitions",
    "rot_piece_def",
    "piece_spawn_height",
]
