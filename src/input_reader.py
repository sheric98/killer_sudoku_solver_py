import json
from typing import Any

from src.constants import SQUARES_KEY, SUM_KEY
from src.group import Group
from src.square import Square


class InputReader:
    def __init__(self, square_map: list[list[Square]]):
        self._square_map = square_map

    def read(self, fname: str) -> list[Group]:
        with open(fname, 'r') as f:
            return [self._obj_to_group(obj) for obj in json.load(f)]

    def from_arr(self, group_arr: list[Any]) -> list[Group]:
        return [self._obj_to_group(obj) for obj in group_arr]

    def _obj_to_group(self, obj: Any) -> Group:
        tot_sum = obj[SUM_KEY]
        squares = obj[SQUARES_KEY]

        group_squares = [self._square_map[r][c] for r, c in squares]
        return Group(group_squares, tot_sum)
