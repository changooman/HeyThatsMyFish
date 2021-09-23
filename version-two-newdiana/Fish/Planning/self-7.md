## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites:

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_

[X] improve Board interpretation including hexagon grid 2D coordinate representation

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/7bcf39db107e9a02d2c704ce54a93ead4192d601)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/7bcf39db107e9a02d2c704ce54a93ead4192d601/Fish/Common/board.py#L10-L19)


- a purpose statement for the "reachable tiles" functionality on the board representation

We lacked a definition of "reachable," so we added one.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/c10535103b26cb7abea7e941a27de1f52756eff3)


- two unit tests for the "reachable tiles" functionality

Our code base correctly addressed this aspect from the beginning and we never received any criticism about it.

[The current state of reachable tiles unit tests](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/bdffa699b41ada2a3b64b13f1bb951de4252d9f8/Fish/Common/Other/Test/test_board.py#L61-L94)


### Game States


- a data definition and an interpretation for the game _state_

[X] improve game state interpretation, specifically the data definition

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/7bcf39db107e9a02d2c704ce54a93ead4192d601)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/7bcf39db107e9a02d2c704ce54a93ead4192d601/Fish/Common/state.py#L4-L11)


- a purpose statement for the "take turn" functionality on states

Our code base correctly addressed this aspect from the beginning and we never received any criticism about it.

[The current state of the take turn functionality purpose statement](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/bdffa699b41ada2a3b64b13f1bb951de4252d9f8/Fish/Common/state.py#L201-L207)


- two unit tests for the "take turn" functionality

We were originally under the impression that "take turn" functionality referred to managing and enforcing turn order, rather than the function we call "move_avatar." This became the following todo list item. We did, however, have unit tests for the "move_avatar" functionality.

[X] add non-trivial turn-taking tests for State and better document existing tests

[Unit Tests](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/bdffa699b41ada2a3b64b13f1bb951de4252d9f8/Fish/Common/Other/Test/test_state.py#L234-L280)


### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games

[X] add explanation of "skip" transitions in game tree interpretation

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/5f9db148a42c26402e2b7122e1ac15576d690895)
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/5f9db148a42c26402e2b7122e1ac15576d690895/Fish/Common/game_tree.py#L7-L8)


- a purpose statement for the "maximin strategy" functionality on trees

Our code base correctly addressed this aspect from the beginning and we never received any criticism about it.

[The current state of the maximin strategy purpose statement](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/bdffa699b41ada2a3b64b13f1bb951de4252d9f8/Fish/Player/strategy.py#L114-L123)


- two unit tests for the "maximin" functionality

Our code base included these tests from the beginning, but we recently revisted and fixed them based on the following todo list item.

[X] look at failed milestone 6 fest.txt tests

[The current state of the maximin strategy unit tests](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/bdffa699b41ada2a3b64b13f1bb951de4252d9f8/Fish/Player/Other/Test/test_strategy.py#L47-L92)


### General Issues

Point to at least two of the following three points of remediation:


- the replacement of `null` for the representation of holes with an actual representation


- one name refactoring that replaces a misleading name with a self-explanatory name

    After being asked to create a Player class, we needed to rename our already existing Player class used by the board to BoardPlayer to avoid conflict and confusion.

    [The BoardPlayer class in the commit in which it was changed](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/913846972d7ddffeb0c410650f13b9743323b337/Fish/Common/board_player.py#L3)


- a "debugging session" starting from a failed integration test:
  - the failed integration test
    - We failed many of the fest tests for milestone 6.
  - its translation into a unit test (or several unit tests)
    - This exposed a fundamental misunderstand of the maximin algorithm and resulted in a change in most unit tests which originally reflected this misunderstanding. We also added additional integration tests.

      [Fix of original unit tests and new integration tests](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/b89449b35b5dd8c4bec1348b7dc35fac70698545)

  - its fix
     - [Bugfix](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/af799e51e1489ae09425d351cbd096e3e6043d76)

  - bonus: deriving additional unit tests from the initial ones
     - If applicable, see the new integration tests linked above.


### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).

  Our original implementations for Player.make_placement() and Player.make_move() took a game state as an input argument and mutated the state with the placement or move. During the next milestone, we actually realized that a better design would be to not mutate the state and instead return the action that the Player would like to take before receiving feedback that these functions neglected to mention this in their purpose statements and reworked it.

todo.md:

[X] specify that the input state is mutated by Player.make_placement() and Player.make_move()

reworked.md:

> the input place_penguin is mutated, hence the user must intimated of it through the purpose statement so that they are aware about this when they use this method.

We did not include in our purpose statements for Strategy move and placement functions that the input state would be mutated. We later reworked our design so that the input state was not mutated.

[Commit](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/913846972d7ddffeb0c410650f13b9743323b337),
[Lines](https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/913846972d7ddffeb0c410650f13b9743323b337/Fish/Player/strategy.py#L27)
