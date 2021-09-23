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


    def __minimax_val_helper(self, children, curr_color, n, is_max_turn):
        """Helper function to compute the minimax value. Will compute the minimax
        value or either the maximizing player or one of the minimizing players,
        depending on what is specified.

        children (list): the a list of GameTreeNode that are the evaluated children
           of the node we are calculating the minimax value for.
        curr_color (str): the color of the player to perform minimax for.
        n (int): the depth of the search tree to search.
        is_max_turn (bool): True if the parent of the child nodes is the maximizing player,
            False otherwise.
        
        returns (int): the minimax value for the parent of the given child nodes
        """
        if is_max_turn:
            max_val = float('-inf')
            for child in children:
                val = self.__minimax_val(child, curr_color, n-1)
                if val > max_val:
                    max_val = val
            return max_val
        else:
            min_val = float('inf')
            for child in children:
                val = self.__minimax_val(child, curr_color, n)
                if val < min_val:
                    min_val = val
            return min_val

    def __minimax_val(self, node, curr_color, n):
        """Compute the minimax value for this state in the game tree.

        
        tree (GameTreeNode): the game tree node to start at
        curr_color (str): the color of the player to perform minimax for.
        n (int): the depth of the search tree to search.
        
        returns (int): the minimax value for this state in the game tree.
        """

        state = node.get_state()

        if state.is_game_over() or n == 0:
            players = state.get_players()
            player = [p for p in players if p.get_color() == curr_color][0]
            return player.get_score()
        
        # the parent moves of these children are from players with the color of
        # state.whose_turn().get_color()
        children = node.get_children()

        if len(children) == 0:
            state.pass_turn_if_applicable()
            new_node = GameTreeNode(state)
            return self.__minimax_val(new_node, curr_color, n)
            
        is_max_turn = state.whose_turn().get_color() == curr_color
        return self.__minimax_val_helper(children, curr_color, n, is_max_turn)


    def __minimax(self, tree, curr_color, n):
        """Perform minimax from the state in the given tree, for the player
        of the given color. Search the game tree for a depth of `n`.

        tree (GameTreeNode): the game tree node to start at
        curr_color (str): the color of the player to perform minimax for.
        n (int): the depth of the search tree to search.
        """

        children = tree.get_children()
        max_val = float('-inf')
        best = []

        for i, child in enumerate(children):
            new_val = self.__minimax_val(child, curr_color, n-1)

            if new_val > max_val:
                max_val = new_val
                best = [child.get_parent_move()]
            elif new_val == max_val:
                best.append(child.get_parent_move())

        return best

    @staticmethod
    def __filter(moves, key):
        """Helper method to find the smallest value of a specific value of a move in the
        list of moves.

        moves (list): a list of moves in the form ((from_row, from_col), (to_row, to_col))
        key (function): the function used to get the specific value from move. This function should
            take in a move in the form ((from_row, from_col), (to_row, to_col)) and return an integer.

        return (list): a list of moves with the lowest value specified by the given key
        """

        lowest_by_key_num = key(min(moves, key=key))
        lowest_by_key_pos = list(filter(lambda x: key(x) == lowest_by_key_num, moves))

        return lowest_by_key_pos

    def __break_tie(self, moves):
        """Iterate through the list of moves and find the move with:
        
        * the smallest row value in the source coordinate.
        * the smallest col value in the source coordinate.
        * the smallest row value in the target corrdinate.
        * the smallest col value in the target coordinate.

        moves (list): a list of moves ((from_row, from_col), (to_row, to_col))

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col))
        """

        # filter by best 'from' tile
        lowest_from_row = self.__filter(moves, lambda x: x[0][0])
        if len(lowest_from_row) == 1:
            return lowest_from_row[0]
        lowest_from_col = self.__filter(lowest_from_row, lambda x: x[0][1])
        if len(lowest_from_col) == 1:
            return lowest_from_col[0]
            
        # filter by best 'to' tile
        lowest_to_row = self.__filter(lowest_from_col, lambda x: x[1][0])
        if len(lowest_to_row) == 1:
            return lowest_to_row[0]
        lowest_to_col = self.__filter(lowest_to_row, lambda x: x[1][1])
        return lowest_to_col[0]

    def make_move(self, state, n):
        """Make a move based on the best possible gain after n turns of the current
        player, assuming all opponents choose moves that minimize our gain.

        state:  The game State to make the move in.
        n:      The number of turns to look ahead, must be > 0.

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col)), None if no move can be made
        """

        if n <= 0:
            raise ValueError("n must be > 0.")

        p_color = state.whose_turn().get_color()
        tree = GameTreeNode(state)
        
        best = self.__minimax(tree, p_color, n)

        if len(best) == 0:
            return None
        elif len(best) == 1:
            return best[0]
        else:
            return self.__break_tie(best)
            
