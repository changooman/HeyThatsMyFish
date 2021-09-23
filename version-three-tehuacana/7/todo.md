[X] improve game state interpretation, specifically the data definition

[X] improve Board interpretation including hexagon grid 2D coordinate representation

[X] look at failed milestone 4 exe-feedback.txt

[X] look at failed milestone 4 test-feedback.txt

[X] look at failed milestone 4 fest.txt

[X] look at failed milestone 5 test-feedback.txt

[X] look at failed milestone 6 test-feedback.txt

[X] look at failed milestone 6 fest.txt tests

[X] update purpose statement for reachable-positions to define "reachable"

[X] add State.get_reachable() unit tests

[X] add non-trivial turn-taking tests for State and better document existing tests

[X] add explanation of "skip" transitions in game tree interpretation

[X] specify that the input state is mutated by Player.make_placement() and Player.make_move()

[X] specify behavior when Player.make_placement() or Player.make_move() cannot take a valid action

[X] factor out sub-tasks of reachable-positions

[ ] rework GameTreeNode to be able to represent three kinds of nodes: game-is-over, current-player-is-stuck, current-player-can-move

[ ] pull rule checking functionality out of State and into the game tree, have Referee use the game tree for rule checking
