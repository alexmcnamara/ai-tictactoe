"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns: board (list of rows) of the starting state of the game.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns: player who has the next turn on a board i.e. X or O.
    """
    # Count the number of X's and O's on the board
    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)

    if num_X > num_O:
        return O
    if num_O == num_X:
        return X
    else:
        raise ValueError("number of X's and 0's is not possible")
    


def actions(b):
    """
    Returns: set of all possible actions (i, j) available on the board.
    """
    
    actions_set = set()
    empty_board = initial_state()

    for row in range(len(b)):
        for col in range(len(b[row])):
            if b[row][col] == EMPTY:
                # Convert list to tuples to enter set
                actions_set.add((row, col))
    return actions_set


def result(board, action):
    """
    Return: board that results from making move (i, j) on the board.

    Inputs:
    board: current state of the board
    action: possible action that can be taken on board
    """
    # Define action location and player
    i, j = action
    current_player = player(board)

    # Check if the action is valid
    if board[i][j] != EMPTY:
        raise ValueError("Invalid action: Cell already occupied")
    
    # Create deep copy of board
    new_board = copy.deepcopy(board)
    #Update deep copy
    new_board[i][j] = current_player
    return new_board
    

def winner(board):
    """
    Returns the winner of the game (X or O) or None if game is still in play.

    Input:
    board: current state of the game
    """
    # Check if player won horizontally / vertically / diagonally
    for i in range (len(board)):
        # Horizontal
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
        # Vertical
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]
        
    # Check Diagonals    
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    
    else:
        return None


def terminal(board):
    """
    Returns: True if game is over, False otherwise.
    """
    # Check if there is a winner
    winning_player = winner(board)
    # If winning player, game is over
    if winning_player is not None:
        return True 
    # If there are no possible actions i.e. baord is full, game is over.
    if not actions(board):
        return True
    # If no winner yet
    if winning_player == None:
        return False
    
    raise ValueError('Unable to determine if game is terminated')



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    # Check game is finished
    if terminal(board):
        if winning_player == X:
            return 1
        if winning_player == O:
            return -1 
        else:
            return 0
    else:
        return None

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    Inputs:
        board: current state of the board

    Returns:
        The optimal action (i, j) for the player to move on that board,
        or None if the board is a terminal board
    """
    # Base case: if the board is terminal, return None
    if terminal(board):
        return None

    # Get the current player
    current_player = player(board)

    # Maximize for X, minimize for O
    if current_player == X:
        best_score = float('-inf')
        best_action = None
        for action in actions(board):
            player_board = result(board, action)
            score = min_value(player_board)
            if score > best_score:
                best_score = score
                best_action = action
            
    if current_player == O:
        best_score = float('inf')
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = max_value(new_board)
            if score < best_score:
                best_score = score
                best_action = action
    return best_action

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

