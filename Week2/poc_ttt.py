"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 50   # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    move to next available space and then switch player
    """
    while board.check_win() == None:
        randmove = random.randrange(len(board.get_empty_squares()))
        next1 = board.get_empty_squares()[randmove]
        board.move(next1[0], next1[1], player)
        player = provided.switch_player(player)
                                            
def mc_update_scores(scores, board, player):
    """
    update scores
    """
    if board.check_win() == player :
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += MCMATCH
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] -= MCOTHER 
    elif board.check_win() == None :
        return
    elif board.check_win() == provided.DRAW:
        return
    else:
        for row_index in range(board.get_dim()):
            for col_index in range(board.get_dim()):
                if board.square(row_index, col_index) == player:  
                    scores[row_index][col_index] -= MCMATCH
                elif board.square(row_index, col_index) == provided.EMPTY:  
                    scores[row_index][col_index] += 0
                else:
                    scores[row_index][col_index] += MCOTHER


def get_best_move(board, scores):
    """
    find the best move
    """
    
    if len(board.get_empty_squares()) == 0:  # no available moves
        return

    avail = []
    for move in board.get_empty_squares():
        avail.append(scores[move[0]][move[1]])

    best = max(avail)
    poss_moves = []
    index = 0
    while index < len(avail):
        if avail[index] == best:
            poss_moves.append(board.get_empty_squares()[index])
        index += 1
    return random.choice(poss_moves)

def mc_move(board, player, trials):
    """
    =- =
    """
    num = trials
    scores = [[[] for row in range(board.get_dim())] for col in range(board.get_dim())]

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            scores[row][col] = 0
            
    while num:
        board1 = board.clone()
        mc_trial(board1, player)
        mc_update_scores(scores, board1, player)
        num -= 1


    next_move = get_best_move(board, scores)

    return next_move
    
 



# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


#import user35_PIk21NjpAa_0 as tests

#tests.test_mc_trial(mc_trial)                                             # tests for mc_trial

#tests.test_mc_update_scores(mc_update_scores, MCMATCH, MCOTHER)           # tests for mc_update_scores

#tests.test_get_best_move(get_best_move)                                   # tests for get_best_move

#tests.test_mc_move(mc_move, NTRIALS)      
