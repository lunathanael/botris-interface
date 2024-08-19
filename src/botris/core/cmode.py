from typing import TYPE_CHECKING

from botris._core import Botris

from .cconstants import CspinType


class CBotris:
    """
    A Python interface for the C++ Botris class, a class holding
    the game options.

    Attributes:
    -----------
    combo_table : List[int]
        The combo table.
    attack_table : List[int]
        The attack table.
    all_spin_bonus : int
        The all-spin bonus.
    pc_bonus : int
        The perfect clear bonus.
    b2b_bonus : int
        The back-to-back bonus.

    Methods:
    --------
    __init__(self)
        Initialize the Botris class.
    points(self, linesCleared: int, spin: CspinType, pc: bool, combo: int, b2b: int) -> int
        Calculate the points based on the number of lines cleared, spin type, and other factors.
    """

    combo_table: list[int] = Botris.combo_table
    attack_table: list[int] = Botris.attack_table
    all_spin_bonus: int = Botris.all_spin_bonus

    pc_bonus: int = Botris.pc_bonus
    b2b_bonus: int = Botris.b2b_bonus

    def __init__(self):
        """
        Initialize the Botris class.
        """
        pass

    def points(
        self, lines: int, spin: CspinType, pc: bool, combo: int, b2b: int
    ) -> int:
        """
        Calculate the points based on the number of lines cleared, spin type, and other factors.

        Parameters:
        -----------
        linesCleared : int
            The number of lines cleared.
        spin : CspinType
            The spin type.
        pc : bool
            Whether the piece is a perfect clear.
        combo : int (u32)
            The current combo count.
        b2b : int (u32)
            The current back-to-back count.

        Returns:
        --------
        int (size_t)
            The number of points earned.
        """
        pass


if not TYPE_CHECKING:
    CBotris = Botris

__all__ = ["CBotris"]
