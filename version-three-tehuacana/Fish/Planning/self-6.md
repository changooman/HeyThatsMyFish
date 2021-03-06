## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*,
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"

<https://github.ccs.neu.edu/CS4500-F20/purmela/blob/38a643f292709f6f2443a9a9fbe6250a50369731/Fish/Admin/referee.py#L109-L114>

- a unit test for the "place all penguins" funtionality

<https://github.ccs.neu.edu/CS4500-F20/purmela/blob/38a643f292709f6f2443a9a9fbe6250a50369731/Fish/Admin/Other/Test/test_referee.py#L202-203>

- the "loop till final game state"  function

<https://github.ccs.neu.edu/CS4500-F20/purmela/blob/38a643f292709f6f2443a9a9fbe6250a50369731/Fish/Admin/referee.py#L72-L120>

- this function must initialize the game tree for the players that survived the start-up phase


- a unit test for the "loop till final game state"  function

<https://github.ccs.neu.edu/CS4500-F20/purmela/blob/38a643f292709f6f2443a9a9fbe6250a50369731/Fish/Admin/Other/Test/test_referee.py#L195-L206>

- the "one-round loop" function


- a unit test for the "one-round loop" function


- the "one-turn" per player function


- a unit test for the "one-turn per player" function with a well-behaved player


- a unit test for the "one-turn" function with a cheating player


- a unit test for the "one-turn" function with an failing player


- for documenting which abnormal conditions the referee addresses

<https://github.ccs.neu.edu/CS4500-F20/purmela/blob/38a643f292709f6f2443a9a9fbe6250a50369731/Fish/Admin/referee.py#L77-L78>

- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing



**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "38a643f292709f6f2443a9a9fbe6250a50369731".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/purmela/tree/38a643f292709f6f2443a9a9fbe6250a50369731/Fish>

