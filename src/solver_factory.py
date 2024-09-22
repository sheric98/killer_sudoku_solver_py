from typing import Any, Callable

from src.constants import MAX_NUMBER, SMALL_SQUARE_SIZE
from src.input_reader import InputReader
from src.group import Group
from src.group_possibilities import MAX_SUM
from src.solver import Solver
from src.square import Square


def create_init_solver_from_file(groups_file: str) -> Solver:
    return _create_init_solver(lambda input_reader: input_reader.read(groups_file))


def create_init_solver_from_arr(groups_arr: list[Any]) -> Solver:
    return _create_init_solver(lambda input_reader: input_reader.from_arr(groups_arr))


def _create_init_solver(read_groups: Callable[[InputReader], list[Group]]) -> Solver:
    squares = [[Square((i, j)) for j in range(MAX_NUMBER)] for i in range(MAX_NUMBER)]

    row_groups = [Group(row, MAX_SUM) for row in squares]
    col_groups = [Group([row[i] for row in squares], MAX_SUM) for i in range(MAX_NUMBER)]
    small_square_coords = [[(i, j) for i in range(x, x + SMALL_SQUARE_SIZE) \
                            for j in range(y, y + SMALL_SQUARE_SIZE)]
                            for x in range(0, MAX_NUMBER, SMALL_SQUARE_SIZE) \
                                for y in range(0, MAX_NUMBER, SMALL_SQUARE_SIZE)]
    small_square_groups = [Group([squares[i][j] for i, j in coords], MAX_SUM) for coords in small_square_coords]

    input_reader = InputReader(square_map=squares)
    groups = read_groups(input_reader) + row_groups + col_groups + small_square_groups

    squares_set = set(sq for row in squares for sq in row)

    return Solver(squares_set, set(groups))



