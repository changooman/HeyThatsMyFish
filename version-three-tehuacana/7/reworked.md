#

> -15 insufficient interpretation of the game state
> (it should be clear
> what all components of the data definition mean,
> how players are related to penguins and how penguins' locations are tracked,
> how players take turns)

We had essentially no state interpretation, so we added a description of the data definition and an interpretation of each element.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/7bcf39db107e9a02d2c704ce54a93ead4192d601)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/7bcf39db107e9a02d2c704ce54a93ead4192d601/Fish/Common/state.py#L4-L11)

#

> -10 insufficient interpretation of the board
> (it should be clear what coordinates mean
> i.e how a position maps to a hexagonal tile on the board)

We lacked a clear coordinate system explanation, so we added a diagram.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/7bcf39db107e9a02d2c704ce54a93ead4192d601)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/7bcf39db107e9a02d2c704ce54a93ead4192d601/Fish/Common/board.py#L10-L19)

#

> -5 purpose statement for reachable-positions does not define "reachable"

We lacked a definition of "reachable," so we added one.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/c10535103b26cb7abea7e941a27de1f52756eff3)

#

> Not a feedback item.

We found that we lacked tests for the get_reachable() function in State, so we added some.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/cdbf65be50e853c40e6c1074ba20da1be6eb64e4)

#

> -7 unit tests for turn-taking functionality
> Player turns are not fully tested. Trivial tests are added, which are not very clear.

After improving our descriptions of each test, we felt that turn taking functionality was adequately tested.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/50318805fc3975fb99b85f06b8f65ff3609e20fd)

#

> -10 data definition/interpretation of the game tree doesn't mention
> how "skip" transitions are dealt with
> (the reader of your code should be able to understand this
> without inspecting the code that generates child trees)

We were missing a description of how the game tree deals with skip transitions; we added one.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/5f9db148a42c26402e2b7122e1ac15576d690895)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/5f9db148a42c26402e2b7122e1ac15576d690895/Fish/Common/game_tree.py#L7-L8)

#

> the input place_penguin is mutated, hence the user must intimated of it through the purpose statement so that they are aware about this when they use this method.

We did not include in our purpose statements for Strategy move and placement functions that the input state would be mutated. We later reworked our design so that the input state was not mutated.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/913846972d7ddffeb0c410650f13b9743323b337)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/913846972d7ddffeb0c410650f13b9743323b337/Fish/Player/strategy.py#L27)

#

> The make_move is supposed to tell how the system behaves when penguin is stuck hence movement for penguin is skipped. And purpose statement is unclear about what happens when current player does not have valid moves.

Our purpose statements in Strategy lacked descriptions of behavior when a move could not be made; we added them.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/913846972d7ddffeb0c410650f13b9743323b337)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/913846972d7ddffeb0c410650f13b9743323b337/Fish/Player/strategy.py#L19)

#

> -10 sub-tasks of reachable-positions functionality are not factored-out
> (e.g. tracing all reachable positions in some direction, calculating the next coordinate in some direction)

We had some repeating code for traveling in various direction on the board when searching for reachable positions; we factored it out with another helper function.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/c8f1c30f8c4fb6f264956bee98c75bd479fb3269)
