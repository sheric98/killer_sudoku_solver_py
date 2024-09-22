from typing import Optional, Self

from src.group_possibilities import get_group_possibilities
from src.square import Square


class Group:
    def __init__(self, squares: list[Square], total_sum: int, possibles: Optional[list[set[int]]]=None):
        self._squares = set(squares)
        self._total_sum = total_sum

        if possibles is None:
            self._possibles = [set(possible) for possible in get_group_possibilities(len(squares), total_sum)]
            self._update_squares()
        else:
            self._possibles = possibles

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return id(self) == id(other)
    
    def completed(self, square: Square, number: int) -> tuple[list[Square], list[Square], bool]:
        self._squares.remove(square)
        self._total_sum -= number

        self._possibles = [possible for possible in self._possibles if number in possible]
        for possible in self._possibles:
            possible.remove(number)

        if len(self._squares) == 0:
            return [], [], True
        completed, impossible = self._update_squares()

        return completed, impossible, False      

    def copy(self, updated_squares: dict[Square, Square]) -> Self:
        squares = [updated_squares[square] for square in self._squares]

        possibles = [s.copy() for s in self._possibles]
        return Group(squares, self._total_sum, possibles)
            
    def _update_squares(self) -> tuple[list[Square], list[Square]]:
        complete_possibles = set()
        for possible in self._possibles:
            complete_possibles.update(possible)

        completed: list[Square] = []
        impossible: list[Square] = []

        for square in self._squares:
            res = square.reduce_possibles(complete_possibles)

            if res == 0:
                completed.append(square)
            elif res == -1:
                impossible.append(square)

        return completed, impossible