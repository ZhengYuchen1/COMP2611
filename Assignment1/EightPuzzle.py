from copy import deepcopy
from bbmodcache.bbSearch import SearchProblem

def number_position_in_layout( n, layout):
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val==n:
                return (i,j)

class EightPuzzle( SearchProblem ):
    action_dict = {
        (0,0) : [(1, 0, 'up'),    (0, 1, 'left')],
        (0,1) : [(0, 0, 'right'), (1, 1, 'up'),    (0, 2, 'left')],
        (0,2) : [(0, 1, 'right'), (1, 2, 'up')],
        (1,0) : [(0, 0, 'down'),  (1, 1, 'left'),  (2, 0, 'up')],
        (1,1) : [(1, 0, 'right'), (0, 1, 'down'),  (1, 2, 'left'), (2, 1, 'up')],
        (1,2) : [(0, 2, 'down'),  (1, 1, 'right'), (2, 2, 'up')],
        (2,0) : [(1, 0, 'down'),  (2, 1, 'left')],
        (2,1) : [(2, 0, 'right'), (1, 1, 'down'),  (2, 2, 'left')],
        (2,2) : [(2, 1, 'right'), (1, 2, 'down')]
    }
    
    
    def __init__(self, initial_layout, goal_layout ):
        pos0 = number_position_in_layout( 0, initial_layout )
        # Initial state is pair giving initial position of space
        # and the initial tile layout.
        self.initial_state = ( pos0, initial_layout)
        self.goal_layout   = goal_layout
        

    ### I just use the position on the board (state[0]) to look up the 
    ### appropriate sequence of possible actions.
    def possible_actions(self, state ):
        actions =  EightPuzzle.action_dict[state[0]]
        actions_with_tile_num = []
        for r, c, d in actions:
            tile_num = state[1][r][c] ## find number of moving tile
            # construct the action representation including the tile number
            actions_with_tile_num.append( (r, c, (tile_num,d)) )
        return actions_with_tile_num

    def successor(self, state, action):
        old0row, old0col  =  state[0]    # get start position
        new0row, new0col, move = action  # unpack the action representation
        moving_number, _ = move
        ## Make a copy of the old layout
        newlayout = deepcopy(state[1])
        # Swap the positions of the new number and the space (rep by 0)
        newlayout[old0row][old0col] = moving_number
        newlayout[new0row][new0col] = 0
        return ((new0row, new0col), newlayout )
    
    def goal_test(self,state):
        return state[1] == self.goal_layout
    
    def display_action(self, action):
        _,_, move = action
        tile_num, direction = move
        print("Move tile", tile_num, direction)
        
    def display_state(self,state):
        for row in state[1]:
            nums = [ (n if n>0 else '.') for n in row]
            print( "   ", nums[0], nums[1], nums[2] )