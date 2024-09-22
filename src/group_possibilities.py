from src.constants import MAX_NUMBER

MAX_GROUP_SIZE = MAX_NUMBER

MAX_SUM = (MAX_GROUP_SIZE * (MAX_GROUP_SIZE + 1)) // 2

_possibilities_dp: list[list[set[tuple[int, ...]]]] = [[set() for _ in range(MAX_SUM + 1)] for _ in range(MAX_GROUP_SIZE + 1)]

_possibilities_dp[0][0].add(())


for group_size in range(1, MAX_GROUP_SIZE + 1):
    for target_sum in range(1, MAX_SUM + 1):
        for i in range(1, MAX_NUMBER + 1):
            prev_sum = target_sum - i

            if prev_sum < 0:
                continue

            for possibility in _possibilities_dp[group_size - 1][prev_sum]:
                if i in possibility:
                    continue

                new_possibility = list(possibility)
                new_possibility.append(i)
                new_possibility = tuple(sorted(new_possibility))
                _possibilities_dp[group_size][target_sum].add(new_possibility)

def get_group_possibilities(group_size: int, group_sum: int) -> set[tuple[int, ...]]:
    return _possibilities_dp[group_size][group_sum]
