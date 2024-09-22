# Overview

This repository contains code to solve killer sudoku. The logic for now is fairly basic and relies mostly on guessing and checking recursively
(other than calculating initial possibilities based on group size and sum).

# Usage
## CLI
```
python3 main.py --groups_file groups.json
```

Provide a json file containing group information in the format of an array of `{"sum": <group_sum>, "squares": [[<row_idx>, <col_idx>], ...]}` where the indexes are 0-indexed.

The repository contains an example "groups.json" file to try out.

## UI
```
python3 ui.py
```

This UI uses tkinter to generate a board which you can use to select squares and enter the group sum to submit groups before solving.
