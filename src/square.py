from typing import Optional, Self

from src.constants import MAX_NUMBER
from src.coord import Coord


class Square:
    def __init__(self, coord: Coord, possibles: Optional[set[int]]=None):
        self._coord = coord
        if possibles is None:
            self._possibles = set(range(1, MAX_NUMBER + 1))
        else:
            self._possibles = possibles

    def __eq__(self, other: Self) -> bool:
        return self._coord == other._coord

    def __hash__(self):
        return hash(self._coord)
    
    def reduce_possibles(self, possibles: set[int]) -> int:
        self._possibles.intersection_update(possibles)

        if len(self._possibles) == 1:
            return 0
        elif len(self._possibles) == 0:
            return -1
        else:
            return 1
    
    def copy(self) -> Self:
        return Square(self._coord, self._possibles.copy())
