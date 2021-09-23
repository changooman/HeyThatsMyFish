# Fish game tournament system

## Requirements
* python 2.7.5

## Structure
```
.
├── 3
│   ├── Tests
│   │   ├── *-in.json           # xboard test inputs
│   │   └── *-out.json          # xboard test outputs
│   └── xboard                  # Test harness
├── 4
│   ├── Tests
│   │   ├── *-in.json           # xstate test inputs
│   │   └── *-out.json          # xstate test outputs
│   └── xstate                  # Test harness
├── 5
│   ├── Tests
│   │   ├── *-in.json           # xstate test inputs
│   │   └── *-out.json          # xstate test outputs
│   └── xtree                   # Test harness
├── 6
│   ├── Tests
│   │   ├── *-in.json           # xstate test inputs
│   │   └── *-out.json          # xstate test outputs
│   └── xstrategy               # Test harness
├── 7
│   ├── todo.md                 # Milestone 7 TODO list
│   ├── reworked.md             # List of project reworks
│   └── bugs.md                 # List of project bugfixes
├── 8
│   ├── Tests
│   │   ├── *-in.json           # xref test inputs
│   │   └── *-out.json          # xref test outputs
│   └── xref                    # Test harness
└── Fish
    ├── __init__.py             # Python packaging file
    ├── Makefile                # Makefile
    ├── xtest                   # Unit test executable
    ├── Common
    │   ├── Other/Test
    │   │   ├── gui_demo.py             # Visual demo
    │   │   ├── run_tests.sh            # Script to run all test files
    │   │   ├── test_board.py           # Unit tests for Board class
    │   │   ├── test_board_player.py    # Unit tests for BoardPlayer class
    │   │   ├── test_state.py           # Unit tests for State class
    │   │   ├── test_game_tree.py       # Unit tests for GameTreeNode class
    │   │   └── test_tile.py            # unit tests for Tile class
    │   ├── __init__.py         # Python packaging file
    │   ├── board.py            # Board class
    │   ├── *_penguin.png       # Penguin images
    │   ├── state.py            # State class
    │   ├── board_player.py     # BoardPlayer class
    │   ├── game_tree.py        # GameTreeNode class
    │   ├── player_interface.py # The PlayerInterface API
    │   └── tile.py             # Tile class
    ├── Player
    │   ├── Other/Test
    │   │   ├── run_tests.sh        # Script to run all test files
    │   │   ├── test_strategy.py    # Unit tests for Strategy class
    │   │   └── test_player.py      # Unit tests for Player class
    │   ├── __init__.py         # Python packaging file
    │   ├── player.py           # Player class
    │   └── strategy.py         # Strategy class
    ├── Admin
    │   ├── Other/Test
    │   │   ├── run_tests.sh        # Script to run all test files
    │   │   ├── test_referee.py     # Unit tests for Referee class
    │   │   └── test_manager.py     # Unit tests for Manager class
    │   ├── __init__.py          # Python packaging file
    │   ├── manager.py           # Manager class
    │   └── referee.py           # Referee class
    ├── Planning
    │   ├── game-state.md       # Data design for game states
    │   ├── player-protocol.md  # The player protcol description
    │   ├── games.md            # Data design for game tree
    │   ├── milestones.pdf      # Fish game milestone sequence
    │   ├── self-*.md           # Self evaluations
    │   ├── remote.md           # Remove collaboration protocol
    │   └── system.pdf          # Fish game system design
    └── README.md               # This README
```
## Game
### Board Coordinate System
This is an example of a board wiht 5 rows and 3 columns:
```
 _____       _____       _____       _____
/ 0,0 \_____/ 0,1 \_____/ 0,2 \_____/ 0,3 \_____
\_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \_____/ 1,3 \
/ 2,0 \_____/ 2,1 \_____/ 2,2 \_____/ 2,3 \_____/
\_____/ 3,0 \_____/ 3,1 \_____/ 3,2 \_____/ 3,3 \
/ 4,0 \_____/ 4,1 \_____/ 4,2 \_____/ 4,3 \_____/
\_____/ 5,0 \_____/ 5,1 \_____/ 5,2 \_____/ 5,3 \
/ 6,0 \_____/ 6,1 \_____/ 6,2 \_____/ 6,3 \_____/
\_____/     \_____/     \_____/     \_____/
```
## Running
Make the project with `make` in `purmela/Fish`.
Run the visual demo with `python Common/Test/gui_demo.py`.

## Testing
Run all unit tests with the executable `./xtest`.
