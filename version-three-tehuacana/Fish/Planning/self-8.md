## Self-Evaluation Form for Milestone 8

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

1. did you organize the main function/method for the manager around
the 3 parts of its specifications --- point to the main function

* <https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/ee2e1aa0c60f17df2d22c503af03c521c7e3eefe/Fish/Admin/manager.py#L55-L68>

2. did you factor out a function/method for informing players about
the beginning and the end of the tournament? Does this function catch
players that fail to communicate? --- point to the respective pieces

* <https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/ee2e1aa0c60f17df2d22c503af03c521c7e3eefe/Fish/Admin/manager.py#L182-L227>

3. did you factor out the main loop for running the (possibly 10s of
thousands of) games until the tournament is over? --- point to this
function.

  * We factored out as much functionality (running a single round, checking if the tournament is over, etc) as we could - however the main loop occurs in out "main" run function.

  * <https://github.ccs.neu.edu/CS4500-F20/newdiana/blob/ee2e1aa0c60f17df2d22c503af03c521c7e3eefe/Fish/Admin/manager.py#L55-L68>

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "ee2e1aa0c60f17df2d22c503af03c521c7e3eefe".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/newdiana/tree/ee2e1aa0c60f17df2d22c503af03c521c7e3eefe/Fish>

