# Purpose: Represents a tournament manager of a single tournament. It initially takes in a list of players who are a
# part of the tournament but players can join and leave before the tournament starts. A set of brackets are created
# once the tournament starts and many games are run until a winner or winners are decided in the final bracket.
class TournamentManager:
    def __init__(self, Players, Referee):
        self.observer_list = []  # the list of observers that is already watching the game
        self.players_list = Players
        self.referee = Referee


# Purpose: Allows a player to join the tournament
# @param player A Player object that represents the player wanting to join
def join_tournament(self, player):
    self.players.append(player)


# Purpose: Allows a player to leave the tournament and forfeit their position
# @param player A Player object that represents the player wanting to join
def leave_tournament(self, player):
    self.players.remove(player)


# Purpose: Lays the foundation for the tournament by forming the tournament bracket
# once the tournament starts
# @param player_list A list of Player objects who initially showed interest
def tournament_bracket(self, player_list):
    # Form the starting brackets
    return

# Purpose: Creates a game for a list of players and runs the game itself
# @param player_list A list of Player objects who initially showed interest
# @return winner_list A list of Player object(s) who won the game
def create_game(player_list):
    # Create a game from the list of players
    # Automate the game and return list of players
    return



# Purpose: Commences the tournament and runs the tournament until completion.
# @return winner_list A list of Player object(s) who won the tournament
def start_tourney():
    # Take the winners from the starting bracket and move them into a next
    # set of brackets
    # Run the process until reaching the end
    winners = []
    # for players in a branch
    # winners.append(self.referee.referee(style, penguins))
    return winners


# Purpose: Allows new observers to join in watching the tournament by adding their
# instance to the list of observers already watching
# @param new_observer, the instance of an observer that wishes to watch the
# tournament that is currently in play
def add_observers(self, new_observer):
    self.observer_list.append(new_observer)


# @param observer, the instance of an observer that wishes to stop watching the
# tournament that is currently in play
def remove_observers(self, observer):
    self.observer_list.remove(observer)
