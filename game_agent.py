"""This file contains all the classes you must complete for this project.
    
    You can use the test cases in agent_test.py to help during development, and
    augment the test suite with your own test cases to further test your code.
    
    You must test your agent's strength against a set of agents with known
    relative strength using tournament.py and include the results in your report.
    """
import random

track = 0

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
        of the given player.
        
        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.
        
        Parameters
        ----------
        game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
        
        player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
        
        Returns
        -------
        float
        The heuristic value of the current game state to the specified player.
        """
    # TODO: finish this function!
        return float(len(game.get_legal_moves()) - (len(game.get_blank_spaces()) - len(game.get_legal_moves())))



class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
        and a depth-limited minimax algorithm with alpha-beta pruning. You must
        finish and test this player to make sure it properly uses minimax and
        alpha-beta to return a good move before the search time limit expires.
        
        Parameters
        ----------
        search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
        
        score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
        
        iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).
        
        method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().
        
        timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
        """
    
    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
    
    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
            result before the time limit expires.
            
            This function must perform iterative deepening if self.iterative=True,
            and it must use the search method (minimax or alphabeta) corresponding
            to the self.method value.
            
            **********************************************************************
            NOTE: If time_left < 0 when this function returns, the agent will
            forfeit the game due to timeout. You must return _before_ the
            timer reaches 0.
            **********************************************************************
            
            Parameters
            ----------
            game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
            
            legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.
            
            time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
            
            Returns
            -------
            (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
            """
        
        self.time_left = time_left
        
        if not legal_moves :
            return(-1,-1)
    
    
        #Get all the moves
        moves = game.get_legal_moves()
        #All non-reflect moves (0,1),(0,3), (1,1),(1,4), (3,0), (3,4), (4,1), (4,3)
        #Unique non-reflect moves for first play
        non_reflect = [(0,1), (1,0)]
        
        #If this is the first play...
        if (len(game.get_legal_moves()) == (game.width * game.height)):
            return (2,2)#game.width // 2, game.height//2)

#If there are a odd number of plays in the game, then we are player1
#and we would have played the center move as the first move so, mirror
if (len(game.get_legal_moves()) %2 != 0):
    mirror_move = reversed(game.get_player_location(game.get_opponent(self)))
        if mirror_move in moves:
            return mirror_move
        
        #If we are player 2:
        
        #Play the center move if possible
        if (game.width // 2, game.height//2) in moves:
            return (game.width // 2, game.height//2)
        
        #Play a move that cannot be mirrored. Only for # of my moves is
        #1 less than the total number of move
        if (((game.width * game.height) - 1) == len(game.get_legal_moves())):
            moves = non_reflect
        
        
        try:
            if (self.method == 'minimax'):
                if self.iterative == True:
                    i = 0
                    while True:
                        _,q = self.minimax(game, i, True)
                        i += 1
                else:
                    _,q = self.minimax(game, self.search_depth, True)
            else:
                if self.iterative == True:
                    i = 0
                    while True:
                        _,q = self.alphabeta(game, i, alpha=float("-inf"),
                                             beta=float("inf"), maximizing_player = True)
                        i += 1
                else:
                    _,q = self.alphabeta(game, self.search_depth,
                                         alpha=float("-inf"), beta=float("inf"),
                                         maximizing_player = True)
                        
                        except Timeout:
                            # Handle any actions required at timeout, if necessary
if q == (-1,-1):
    return moves[0]
        return q
        return q
    
    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.
            
            Parameters
            ----------
            game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
            
            depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
            maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
            
            Returns
            -------
            float
            The score for the current search branch
            
            tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
            
            Notes
            -----
            (1) You MUST use the `self.score()` method for board evaluation
            to pass the project unit tests; you cannot call any other
            evaluation function directly.
            """
        
        #keepMove = (0,0)
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        if (game.utility(self) != 0):
            return game.utility(self),(-1,-1)
        
        #Get all the moves
        moves = game.get_legal_moves()
        
        
        #if there are an odd number of plays in the game
        #if (len(game.get_blank_spaces()) %2 !=0 ):
        
        #If there arn't any moves, return
        #        if(len(moves) < 1):
        #            return float('-inf'),(-1,-1)
        
        #If we are at a terminal state or we have reached max depth, return
        if (depth == 0): #or (game.utility() != 0)
            return self.score(game, self), (-1,-1)
        
        
        #If we at a maximizing node
        if (maximizing_player==True):
            #Set v to the worst possible case for maximizing node
            v = float('-inf')
            #for all of the legal moves for player
            for move in moves:
                q,_ = self.minimax(game.forecast_move(move), depth -1, False)
                if q >= v:
                    v = q
                    keepMove = move
        
        #If we at a minimizing node
        if (maximizing_player==False):
            #Set v to the worst possible case for maximizing node
            v = float('inf')
            #for all of the legal moves for player
            #self.forecast_move(move)
            for move in moves:
                q,_ = self.minimax(game.forecast_move(move), depth -1, True)
                if q <= v:
                    v = q
                    keepMove = move

                        return v, keepMove

def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
    """Implement minimax search with alpha-beta pruning as described in the
        lectures.
        
        Parameters
        ----------
        game : isolation.Board
        An instance of the Isolation game `Board` class representing the
        current game state
        
        depth : int
        Depth is an integer representing the maximum number of plies to
        search in the game tree before aborting
        
        alpha : float
        Alpha limits the lower bound of search on minimizing layers
        
        beta : float
        Beta limits the upper bound of search on maximizing layers
        
        maximizing_player : bool
        Flag indicating whether the current search depth corresponds to a
        maximizing layer (True) or a minimizing layer (False)
        
        Returns
        -------
        float
        The score for the current search branch
        
        tuple(int, int)
        The best move for the current branch; (-1, -1) for no legal moves
        
        Notes
        -----
        (1) You MUST use the `self.score()` method for board evaluation
        to pass the project unit tests; you cannot call any other
        evaluation function directly.
        """
            #keepMove = (0,0)
            
            if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
                
                #Get all the moves
                moves = game.get_legal_moves()
                    
                    if (game.utility(self) != 0):
                        return game.utility(self),(-1,-1)
                            
                            #If there arn't any moves, return
                            #        if(len(moves) < 1):
                            #            return self.score(game,self),(-1,-1)
                            
                            
                            #If we are at a leaf node, return the score
                            if depth == 0:
                                return self.score(game,self), (0,0)
                                    
                                    #If we are at a max branch:
                                    if (maximizing_player==True):
                                        v = float('-inf')
                                            #For every legal move
                                            for move in moves:
                                                #AlphaBeta recursion with min node
                                                q,_ = self.alphabeta(game.forecast_move(move), depth -1, alpha, beta, False)
                                                    #Keep track of the best move
                                                    if (q >= v):
                                                        v = q
                                                            keepMove = move
                                                                #If the value is greater than, equal to, the best one the
                                                                #minimizer can gaurantee, return it as we will never choose
                                                                #this option. The max level will choose the greatest available
                                                                #score however, the min does the opposite.
                                                                if (q >= beta):
                                                                    return q, move   
                                                                        #Alpha is used in the recursive call so we update it with the 
                                                                        #max score
                                                                        alpha = max(alpha, v)
                                                                            
                                                                            #If we are at a min branch:            
                                                                            if (maximizing_player==False):
                                                                                v = float('inf')
                                                                                    #For every legal move
                                                                                    for move in moves:
                                                                                        #AlphaBeta recursion with max node
                                                                                        q,_ = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, True)
                                                                                            #Keep track of the best move
                                                                                            if (q <= v):
                                                                                                v = q
                                                                                                    keepMove = move
                                                                                                        #If the value is less than, equal to,  the best one the 
                                                                                                        #maximizer can gaurantee, return it as we will never choose 
                                                                                                        #this option. The min level will choose the smallest available 
                                                                                                        #score however, the max does the opposite.
                                                                                                        if (q <= alpha):
                                                                                                            return q, move
                                                                                                                #Beta is used in the recursive call so we update it with the 
                                                                                                                #min score
                                                                                                                beta = min(beta, v)
                                                                                                                    return v, keepMove



