# TournamentManager

A TournamentManager class will represent a Fish tournament. The TournamentManager is responsible for creating a round-robin styled bracket using the players who signed up for the tournament.

## Creation

It will be created once the server has finished signing up players at the communication layer. The TournamentManager will be passed a list of players sorted in ascending order by their age.

## Data Representation

The TournamentManager will store the tournament bracket as a 2D array using a Berger Table <https://en.wikipedia.org/wiki/Round-robin_tournament>

## Interface

### __init__(players):

Initialize the TournamentManager by pitting players against each other and stores the bracket in using a round-robin style tournament structure.

### run_tournament():

Runs a tournament by creating a Referee for each game that should be played. Each individual game's players are given to each Referee as a list in ascending order of the players' ages. Once a game is over, the Referee communicates who won the game with the tournament manager, and the tournament manager modifies the bracket accordingly.

### get_victors()

Returns a list of players who won the tournament, or an empty list if the tournament is still underway.

### get_tournament_stats()

Returns statistics collected by the tournament manager - including how many games each player won, average player scores, etc.