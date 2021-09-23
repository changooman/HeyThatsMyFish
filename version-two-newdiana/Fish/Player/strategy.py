from Fish.Common.game_tree import GameTreeNode

class Strategy():
    """A Fish game-playing strategy that can place penguins
    and make moves for any player in the game.
    """

    def make_placement(self, state):
        """Places a penguin on the game board for the current player.
        Attempts to place in the lowest numbered row, then in the lowest numbered column.
        Assumes that the game board is large enough to accommodate all penguins.
        Will do nothing if no open tile is available.

        state:  The game State to place the penguin in.

        returns:    The coordinates of an avatar placement (row, col), None if no placement can be made.
        """
        color = state.whose_turn().get_color()
        board = state.get_board()

        for r in range(board.get_rows()):
            for c in range(board.get_cols()):
                if state.valid_placement((r, c), color):
                    return (r, c)
        return None


    def __get_path(self, node):
        """Debugging function to get the moves leading up to a GameTreeNode.

        node:   The GameTreeNode to print the path of.

        returns:    A string of moves.
        """
        path = ""
        while node.get_parent():
            path = "<" + str(node.get_parent_move()) + ">, " + path
            node = node.get_parent()
        return path


    def __minmax(self, p_color, node, n, debug):
        """Find the child node with the minimum maximum score for a certain player
        after looking ahead n player turns.

        p_color:    The player whose score is being minimized.
        node:       The GameTreeNode to operate at.
        n:          The number of player turns to look ahead.
        debug:      Flag to print debugging statements

        returns:    The minimum maximum score.
        """
        children = node.get_children()
        scores = [self.__next_minimax_func(p_color, child, n, debug) for child in children]

        if len(scores) == 0:
            for player in node.get_state().get_players():
                if player.get_color() == p_color:
                    if debug:
                        print(player.get_score(), self.__get_path(node))
                    return player.get_score()
        else:
            return min(scores)


    def __maxmin(self, p_color, node, n, debug):
        """Find the child node with the maximum minimum score for a certain player
        after looking ahead n player turns.

        p_color:    The player whose score is being minimized.
        node:       The GameTreeNode to operate at.
        n:          The number of player turns to look ahead.
        debug:      Flag to print debugging statements

        returns:    The maximum minimum score.
        """
        if n == 0:
            if debug:
                print(node.get_state().whose_turn().get_score(), self.__get_path(node))
            return node.get_state().whose_turn().get_score()
        else:
            children = node.get_children()
            scores = [self.__next_minimax_func(p_color, child, n-1, debug) for child in children]

        if len(scores) == 0:
            if debug:
                print(node.get_state().get_players()[0].get_score(), self.__get_path(node))
            return node.get_state().whose_turn().get_score()
        else:
            return max(scores)


    def __next_minimax_func(self, p_color, node, n, debug):
        """Choose and evaluate the next minimax function based on whose turn it is.
        If it is p_color's turn, use __maxmin(), otherwise use __minmax().

        p_color:    The player to run minimax for.
        node:       The GameTreeNode to check whose turn it is on.
        n:          The number of player turns to look ahead.
        debug:      Flag to print debugging statements

        returns:    The output score of either function.
        """
        if node.get_state().whose_turn().get_color() == p_color:
            return self.__maxmin(p_color, node, n, debug)
        else:
            node.pass_turn_if_applicable()
            if node.get_state().whose_turn().get_color() == p_color:
                return self.__maxmin(p_color, node, n, debug)
            else:
                return self.__minmax(p_color, node, n, debug)


    def make_move(self, state, n, debug=False):
        """Make a move based on the best possible gain after n turns of the current
        player, assuming all opponents choose moves that minimize our gain.

        state:  The game State to make the move in.
        n:      The number of turns to look ahead, must be > 0.
        debug:  Flag to print debugging statements

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col)), None if no move can be made
        """
        if n <= 0:
            raise ValueError("n must be > 0.")
        p_color = state.whose_turn().get_color()
        children = GameTreeNode(state).get_children()
        if len(children) == 0: return None

        if n == 1:
            scores = []
            for child in children:
                for player in child.get_state().get_players():
                    if player.get_color() == p_color:
                        scores.append(player.get_score())
                        break
        else:
            scores = [self.__next_minimax_func(p_color, child, n-1, debug) for child in children]
        best_score = max(scores)
        best_children = []
        for i in range(len(children)):
            if scores[i] == best_score:
                best_children.append(children[i])
        if debug:
            print('')
            print(n, scores, ["<" + str(child.get_parent_move()) + ">" for child in children])
            print('')
            print('')
        best_children.sort(key=lambda x: (x.get_parent_move()[0][0],
                                          x.get_parent_move()[0][1],
                                          x.get_parent_move()[1][0],
                                          x.get_parent_move()[1][1]))
        return best_children[0].get_parent_move()
