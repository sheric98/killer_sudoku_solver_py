import json

OutputBoard = list[list[int]]


def display_board(board: OutputBoard):
    print('[')
    for i, row in enumerate(board):
        out = f'  {row},'
        print(out)
    print(']')
