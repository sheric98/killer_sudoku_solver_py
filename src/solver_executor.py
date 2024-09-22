from typing import Any, Callable

from src.output_board import OutputBoard
from src.solver import Solver
from src.solver_factory import create_init_solver_from_arr, create_init_solver_from_file


def solve_from_arr(arr: list[Any]) -> list[OutputBoard]:
    return _solve(lambda: create_init_solver_from_arr(arr))


def solve_from_json(json_fname: str) -> list[OutputBoard]:
    return _solve(lambda: create_init_solver_from_file(json_fname))


def _solve(get_solver: Callable[[], Solver]) -> list[OutputBoard]:
    solver = get_solver()
    return solver.solve()