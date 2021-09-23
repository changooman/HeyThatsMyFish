## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*, 
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Player/player.py#L53-L67

- a unit test for the "place all penguins" funtionality 
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L218-L242

- the "loop till final game state"  function
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/referee.py#L47-L72

- this function must initialize the game tree for the players that survived the start-up phase
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Player/player.py#L84-L85

- a unit test for the "loop till final game state"  function
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L13-L37

- the "one-round loop" function
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/referee.py#L66-L70

- a unit test for the "one-round loop" function
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L377-L405

- the "one-turn" per player function
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Player/player.py#L69-L87

- a unit test for the "one-turn per player" function with a well-behaved player 
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L322-L347

- a unit test for the "one-turn" function with a cheating player
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L440-L466

- a unit test for the "one-turn" function with an failing player 
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/Other/referee_tests.py#L468-L497

- for documenting which abnormal conditions the referee addresses 
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Admin/referee.py#L6-L12

- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing 
https://github.ccs.neu.edu/CS4500-F20/queencity/blob/05a89760f97ce734131e55991333b0da9b8763b5/Fish/Player/player.py#L84-L85


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "05a89760f97ce734131e55991333b0da9b8763b5".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/queencity/tree/05a89760f97ce734131e55991333b0da9b8763b5/Fish>

