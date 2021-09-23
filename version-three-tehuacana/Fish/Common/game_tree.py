from copy import deepcopy

class GameTreeNode():
    """Represents an entire game, starting from some state.

    Specifically, this is a tree of possible game states, branching at each possible move until the game end.
    Each node's children are lazily evaluated. Turns can be passed with pass_turn_if_applicable(), after this
    the node's children while be states after all passable turns in a row have been passed.

    self.state:     The State this node is starting from.
    self.children:  A list of valid successive GameTreeNodes 1 valid move after self.state.
                    Is None if not yet evaluated, a list otherwise.
    self.parent:    The parent node, None if root.
    self.parent_move:   The move that lead from the parent node state to this, None if root.
                        In format ((from_x, from_y), (to_x), (to_y)).
    """

    def __init__(self, starting_state, parent=None, parent_move=None):
        """Initialize the GameTree.

        starting_state: The state to start the tree from. All players' penguins must have been placed.
        parent:         The GameTreeNode parent on this node, if it's not the root.
        """
        # if (not starting_state.all_avatars_placed()):
            # raise ValueError("Provided state was not done with placement round.")
        self.state = deepcopy(starting_state)
        self.children = None
        self.parent = parent
        self.parent_move = parent_move


    def __evaluate_children(self):
        """Call for the lazy evaluation of this node's children."""
        if self.children is not None: return
        self.children = []
        player = self.state.whose_turn()
        moves = []
        for penguin in player.get_penguins():
            for dest in self.state.get_reachable(penguin):
                moves.append((penguin, dest))
        if len(moves) > 0:
            for move in moves:
                new_state = deepcopy(self.state)
                new_state.move_avatar(*move)
                self.children.append(GameTreeNode(new_state, self, move))


    def pass_turn_if_applicable(self):
        """Pass the current player's turn if applicable.

        The children will then have to be regenerated, necessitating another call to get_children().
        """
        self.children = None
        self.state.pass_turn_if_applicable()


    def get_parent(self):
        """Get this node's parent node.

        returns:    The parent GameTreeNode.
        """
        return self.parent


    def get_parent_move(self):
        """Get this node's parent move.

        returns:    The parent move in format ((from_x, from_y), (to_x), (to_y)).
        """
        return self.parent_move


    def get_children(self):
        """Get the valid successive GameTreeNodes of this node.

        returns:    A list of all valid successive GameTreeNodes.
        """
        self.__evaluate_children()
        return self.children


    def get_state(self):
        """Get the node's game State.

        returns:    The node's game State.
        """
        return self.state


    def query_action(self, action):
        """Determine legality of action on this node and take it if legal.

        action: A tuple of two coordinate locations ((x1, y1), (x2, y2)),
                the starting and ending locations of a penguin move.

        returns:    None if the action is illegal, the resulting State otherwise.
        """
        if self.state.valid_move(*action):
            new_state = deepcopy(self.state)
            new_state.move_avatar(*action)
            return new_state
        else:
            return None


    def query_function(self, function):
        """Applies a function to all states directly reachable from this node's state.

        function:   A function object that accepts exactly one State as it's argument.

        returns:    A list of the functions return values.
        """
        return [function(child.get_state()) for child in self.get_children()]
