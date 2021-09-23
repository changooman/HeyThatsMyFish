## Self-Evaluation Form for Milestone 9

You must make an appointment with your grader during his or her office
hour to demo your project. See the end of the self-eval for the assigned
grader. 

Indicate below where your TA can find the following elements in your strategy 
and/or player-interface modules: 

1. for human players, point the TA to
   - the interface (signature) that an AI player implements
   - the interface that the human-GUI component implements
   - the implementation of the player GUI

2. for game observers, point the TA to
   - the `game-observer` interface that observers implement
https://github.ccs.neu.edu/CS4500-F20/tehuacana/blob/165b81e60d043f0bb0f98a66e13bede8447d4f43/Fish/Admin/game_visualizer.py#L38-L51
   - the point where the `referee` consumes observers 
We didn't have the referee consume observers as we had the functionality for running an individual round available for the referee. Thus,
we connected the functionality for runnning an individual round to the button in our GUI that advanced turns.
   - the callback from `referee` to observers concerning turns
https://github.ccs.neu.edu/CS4500-F20/tehuacana/blob/165b81e60d043f0bb0f98a66e13bede8447d4f43/Fish/Admin/game_visualizer.py#L160-L175

3. for tournament observers, point the TA to
   - the `tournament-observer` interface that observers implement 
   - the point where the `manager` consumes observers 
   - the callback to observes concerning the results of rounds 


Do not forget to meet the assigned TA for a demo; see bottom.  If the
TA's office hour overlaps with other obligations, sign up for a 1-1.


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "165b81e60d043f0bb0f98a66e13bede8447d4f43".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/tehuacana/tree/165b81e60d043f0bb0f98a66e13bede8447d4f43/Fish>

Assigned grader = Dhaval Dedhia (dedhia.d@northeastern.edu)

