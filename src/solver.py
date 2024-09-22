from collections import defaultdict, deque
from typing import Optional, Self

from src.constants import MAX_NUMBER
from src.group import Group
from src.output_board import OutputBoard
from src.square import Square

NUM_ROWS = MAX_NUMBER
NUM_COLS = MAX_NUMBER


class Solver:
    def __init__(self,
                 squares: set[Square],
                 groups: set[Group],
                 board: Optional[list[list[Optional[int]]]] = None):
        self._square_to_groups: dict[Square, list[Group]] = defaultdict(list)
        for group in groups:
            for square in group._squares:
                self._square_to_groups[square].append(group)
        self._squares = squares
        self._groups = groups

        if board is None:
            self._board = [[None] * NUM_COLS for _ in range(NUM_ROWS)]
        else:
            self._board = board

    def solve(self, determined_square: Optional[Square] = None) -> list[OutputBoard]:
        if determined_square is None:
            if any(len(sq._possibles) == 0 for sq in self._squares):
                return []
            
            determined_squares = set(sq for sq in self._squares if len(sq._possibles) == 1)
        else:
            determined_squares = set((determined_square,))

        while determined_squares:
            to_update: set[Square] = set()
            for sq in determined_squares:
                if not sq._possibles:
                    return []
                num = sq._possibles.pop()
                self._squares.remove(sq)
                self._board[sq._coord[0]][sq._coord[1]] = num

                for group in self._square_to_groups[sq]:
                    complete, impossible, finished_group = group.completed(sq, num)

                if impossible:
                    return []
                
                if finished_group:
                    self._groups.remove(group)
                
                for square in complete:
                    if square in self._squares and square not in determined_squares:
                        to_update.add(square)

            determined_squares = to_update

        if not self._squares:
            return [self._board]
        cand_square = min(self._squares, key=lambda sq: len(sq._possibles))
        res = []
        for possible_num in cand_square._possibles:
            solver_copy, square_copy = self.copy(cand_square)
            square_copy._possibles = {possible_num}
            child_res = solver_copy.solve(determined_square=square_copy)
            res.extend(child_res)

        return res


    def copy(self, start_square: Square) -> tuple[Self, Square]:
        square_map: dict[Square, Square] = {sq: sq.copy() for sq in self._squares}
        
        board = [row.copy() for row in self._board]

        return Solver(set(square_map.values()), set(gr.copy(square_map) for gr in self._groups), board),\
            square_map[start_square]
