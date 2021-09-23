class ManagerProtocol():
	"""An API for the tournament manager to communicate with the referee"""

	"""
	self.bracket:	the tournament data representation as a 2D-array . Contains
        which players will play in each game and who victors play next using a
        round-robin style tournament structure.

	"""
	def __init__(self, players):
		"""Initialize the TournamentManager by pitting players against each other in
                a round-robin styled bracket - the bracket is stored in self.bracket"""
		pass

	def run_tournament(self):
		"""Runs a tournament by creating a Referee for each game instance that should be played.
                Each game's players are given to the Referee in ascending order by the players' ages. Once
                a game is over, the Referee communicates who won the game with the tournament manager, and
                the tournament manager modifies the bracket accordingly.

		"""
		pass

	def get_victors(self):
		"""Gets who won the tournament.

		returns:	a list of players who won the tournament, or an empty list if the
                tournament is still underway.
		"""

	def get_tournament_stats(self):
		"""Gets collected tournament statistics.
		
		returns:	a JSON dictionary of statistics collected by the tournament manager
		"""
