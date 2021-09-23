# FISH README

The numbered folders hold a script that runs their respective test modules, as well as the in and out json files used 
for testing

The Common folder holds all of the program related files. It specifically has the main board.py file which hosts the 
codebase for the FISH game itself. The state.py file which hosts the codebase for the gamestate and player information,
and the game_tree.py file to get a tree of future possible states. It also has the player_inteface.py which is a rough 
design plan for the future assignment. Common also has a subdirectory Other that has .gif images we used for fish 
representation and penguin representation as well as our tester files and copies of files in /Common due to the fact 
that out of directory imports are finicky in python.

The Player folder holds the strategy file and a folder called Other that holds the tests and requirements for 
strategy.py. strategy.py has a function that places penguins in a specific order, and a function that gives the best 
move for a player in a given starting state. Player also has a file called player that has functionality for running the
initial moves in a game (placing the penguins) and the next turn for an individual player

The Admin folder holds the referee file and a folder called other that holds its tests and requirements for referee.py. 
referee.py has the functionality to run a game, determine the winner, and remove a player. It also has the 
manager-interface.py which is sudo-code in preparation for the manager interface that we will create next week.

The Planning folder holds all of the design sided materials. It specifically contains the milestones PDF file which was
our roadmap for the overall project. The system PDF file breaks down the project design into high/low level components.
it also contains our self evaluations and our design plans for the next milestone in game.md, game-state.md, and 
player_protocol.md 

```
3
│   xboard
└───Tests
│   │   1-in.json
│   │   1-out.json
│   │   2-in.json
│   │   2-out.json
│   │   3-in.json
│   │   3-out.json
└───Other
│   │   1.gif
│   │   2.gif
│   │   3.gif
│   │   4.gif
│   │   5.gif
│   │   black.gif
│   │   brown.gif
│   │   red.gif
│   │   white.gif
│   │   fish.py
│   │   state.py
│   │   tester.py
│   │   tester2.py
│   │   xboard.py
4
│   xstate 
└───Tests
│   │   1-in.json
│   │   1-out.json
│   │   2-in.json
│   │   2-out.json
│   │   3-in.json
│   │   3-out.json
└───Other
│   │   1.gif
│   │   2.gif
│   │   3.gif
│   │   4.gif
│   │   5.gif
│   │   black.gif
│   │   brown.gif
│   │   red.gif
│   │   white.gif
│   │   fish.py
│   │   state.py
│   │   tester.py
│   │   tester2.py
│   │   board.py
│   │   game_tree.py
│
5
│   xtree 
└───Tests
│   │   1-in.json
│   │   1-out.json
│   │   2-in.json
│   │   2-out.json
│   │   3-in.json
│   │   3-out.json
└───Other
│   │   1.gif
│   │   2.gif
│   │   3.gif
│   │   4.gif
│   │   5.gif
│   │   black.gif
│   │   brown.gif
│   │   red.gif
│   │   white.gif
│   │   fish.py
│   │   state.py
│   │   tester.py
│   │   tester2.py
│   │   board.py
│   │   game_tree.py
│   │   xtree.py
│
6
│   xstrategy
└───Tests
│   │   1-in.json
│   │   1-out.json
│   │   2-in.json
│   │   2-out.json
│   │   3-in.json
│   │   3-out.json
│   │   4-in.json
│   │   4-out.json
│   │   5-in.json
│   │   5-out.json
└───Other
│   │   1.gif
│   │   2.gif
│   │   3.gif
│   │   4.gif
│   │   5.gif
│   │   black.gif
│   │   brown.gif
│   │   red.gif
│   │   white.gif
│   │   board.py
│   │   game_tree.py
│   │   state.py
│   │   strategy.py
│   │   tester.py
│   │   tester2.py
│   │   xstrategy.py
Fish
│   README.md
│   xtest
└───Admin
│   │   referee.py
│   │   manager-interface.py
│   └───Other
│   │   │   __init__
│   │   │   1.gif
│   │   │   2.gif
│   │   │   3.gif
│   │   │   4.gif
│   │   │   5.gif   
│   │   │   black.gif
│   │   │   brown.gif
│   │   │   red.gif
│   │   │   white.gif
│   │   │   board.py
│   │   │   game_tree.py
│   │   │   player.py
│   │   │   referee.py
│   │   │   referee_tests.py
│   │   │   state.py
│   │   │   strategy.py
│   │   │   strategy_tests.py
│ 
└───Common
│   │   board.py
│   │   game_tree.py
│   │   state.py
│   │   player_interface.py
│   └───Other
│   │   │   1.gif
│   │   │   2.gif
│   │   │   3.gif
│   │   │   4.gif
│   │   │   5.gif   
│   │   │   black.gif
│   │   │   brown.gif
│   │   │   red.gif
│   │   │   white.gif
│   │   │   fish.py
│   │   │   Render.py
│   │   │   state.py
│   │   │   game_tree.py
│   │   │   tester.py
│   │   │   tester2.py
│   │   │   tester3.py
│   │   │   xboard.py 
│ 
└───Player
│   │   strategy.py
│   │   player.py
│   └───Other
│   │   │   __init__.py
│   │   │   board.py
│   │   │   game_tree.py
│   │   │   state.py
│   │   │   strategy.py   
│   │   │   strategy_tests.py 
│
└───Planning
    │   milestones.pdf
    │   system.pdf
    │   self-1.md
    │   self-2.md
    │   self-3.md
    │   self-4.md
    │   self-5.md
    │   game-state.md
    │   games.md
    │   player_protocol.md
    │   manager-protocol.md
    │   referee.md
```

To run tests for individual milestones follow these steps otherwise to run all unit tests run ./xtest

To test the second coded milestone, go to bash command prompt and type out "python tester.py". 
It will return something along the lines of:

Ran 15 tests in 0.752s

OK

To test the third milestone, once again use the bash command prompt to run "python tester2.py"
It will return something along the lines of:

Ran 9 tests in 0.254s

OK

To test the fourth milestone, once again use the bash command prompt to run "python treetest.py"
It will return something along the lines of:

Ran 26 tests in 0.206s

OK

To test the fifth milestone, once again use the bash command prompt to run "python strategy_tests.py" It is however 
located in Fish/Player/Other as opposed to the usual Fish/Common/Other It will return something along the lines of:

Ran 26 tests in 18.517s

OK

To test the sizth milestone, use the bash command prompt to run "python referee_tests.py" It is located in 
Fish/Admin/Other. It will return something along the lines of:


Ran 20 tests in 3.185s

OK