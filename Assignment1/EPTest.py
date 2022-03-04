from bbmodcache.bbSearch import search
from EightPuzzle import EightPuzzle

#SETUP, ignore this
import sys
orig_stdout = sys.stdout
f = open("EPOutput.txt", "w")
sys.stdout = f

import signal
def signal_handler(signum, frame):
    raise Exception("timed out")
signal.signal(signal.SIGALRM, signal_handler)

#HEURISTIC N COST FUNCTIONS N SUCH
def number_position_in_layout( n, layout):
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val==n:
                return (i,j)

def misplaced_tiles(state):
    layout = state[1]
    total = 0
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val==0:
                continue
            if val != GOAL[i][j]:
                total += 1
    return total

def manhattan(state):
    layout = state[1]
    total = 0
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val==0:
                continue
            trueX = int((val -1) /3)
            trueY = (val-1) % 3
            total += abs(i - trueX) + abs(j - trueY)
    return total


def cost(path, state):
    return len(path)

# function arguments to show less debug info on screen
kwargs = {"show_path":False, "show_state_path":False, "dots":True}
maxNodes = 1000000

GOAL = [[1,2,3],
        [4,5,6],
        [7,8,0]]

#3 steps away
TEST_1 = [  [1,0,3],
            [4,2,6],
            [7,5,8]]

#10 steps away
TEST_2 = [  [4,1,3],
            [2,0,8],
            [7,6,5] ]

TEST_3 = [  [2,5,4],
            [1,8,7],
            [0,6,3] ]



testCases = [   {"mode":"BF", "max_nodes":maxNodes, "loop_check":False, "randomise":False, "heuristic":None,            "cost":None}, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":None,            "cost":None},

                {"mode":"DF", "max_nodes":100000,   "loop_check":False, "randomise":False, "heuristic":None,            "cost":None}, 
                {"mode":"DF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":None,            "cost":None}, 
                {"mode":"DF", "max_nodes":maxNodes, "loop_check":True,  "randomise":True,  "heuristic":None,            "cost":None},

                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":misplaced_tiles, "cost":None}, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":manhattan,       "cost":None}, 

                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":misplaced_tiles, "cost":cost}, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":manhattan,       "cost":cost}]


TIME_LIMIT = 2 * 60
INITIAL_STATES = [TEST_1, TEST_2, TEST_3]

for x, INITIAL_STATE in enumerate(INITIAL_STATES):
    EP = EightPuzzle(INITIAL_STATE, GOAL)
    print("\n**********RUNNING TEST CASES FOR INITIAL STATE: ", x+1, "**********")

    for y, testArgs in enumerate(testCases):
        print("\n*****RUNNING TEST", y+1, "WITH ARGS:" , testArgs)

        signal.alarm(TIME_LIMIT)
        try:
            search(EP, **testArgs, **kwargs)
        except:
            print("TIMEOUT")

print("\n\n******FINISHED******")
sys.stdout = orig_stdout
f.close()
print("\n\n******FINISHED******")
