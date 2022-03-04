from bbmodcache.bbSearch import search
from RobotWorker import Door, Robot, State, RobotWorker, ITEM_WEIGHT
import math

# SETUP, ignore this
import sys
import signal
orig_stdout = sys.stdout
f = open("RWOutput.txt", "w")
sys.stdout = f
def signal_handler(signum, frame):
    raise Exception("timed out")
signal.signal(signal.SIGALRM, signal_handler)


#INITIAL STATE SETUP
ROOM_CONTENTS = {
    'workshop'      : {'rusty key'},
    'store room'    : {'bucket', 'suitcase'},
    'tool cupboard' : {'sledge hammer', 'anvil', 'screwdriver', 'keycard'},
    'office'        : {'backpack', "iron key"}
}
DOORS = [
    Door('workshop', 'store room' ),
    Door( 'store room', 'tool cupboard', doorkey='rusty key', locked=True ),
    Door('workshop', 'office', doorkey='keycard', locked=True),
]
rob = Robot('store room', [], 15 )
state = State(rob, DOORS, ROOM_CONTENTS)

goal_1 =  {"store room":{"sledge hammer", "screwdriver"}}
goal_2 =  {"store room":{"sledge hammer", "screwdriver"}, "workshop":{"keycard", "anvil"}}
goal_3 =  {"store room":{"sledge hammer", "screwdriver"}, "workshop":{"keycard", "anvil", "backpack"}, "tool cupboard":{"iron key"}}
   
def misplaced_items(state):
    robotThings = state.robot.carried_items
    robotLoc = state.robot.location
    cost = 0

    for loc in goal_item_locations:
        for item in goal_item_locations[loc]:
            if item not in state.room_contents[loc]:

                if item not in robotThings or robotLoc != loc:
                    cost += 2*ITEM_WEIGHT[item]
                    if item in robotThings:
                        cost -= ITEM_WEIGHT[item]
    return cost

def minimum_trips(state):
    strength = state.robot.strength
    robotThings = state.robot.carried_items
    robotLoc = state.robot.location
    cost = 0
    for loc in goal_item_locations:
        load = 0
        for thing in goal_item_locations[loc]:
            if thing not in state.room_contents[loc]:
                if thing not in robotThings or robotLoc != loc:
                    cost += 2*ITEM_WEIGHT[thing]
                    load += ITEM_WEIGHT[thing]
                    if thing in robotThings:
                        cost -= ITEM_WEIGHT[thing]
        trips = 2 * math.ceil(load/strength) -1
        if robotLoc == loc or load == 0:
            trips += 1
        cost += trips * strength
    return cost

def simpleCost(path, state):
    return len(path)

def weightedCost(path, state):
    load = state.robot.weight_carried()
    cost = 0
    strength = state.robot.strength

    for action, thing in path[::-1]:
        if action == "move to":
            cost += strength + load
        elif action == "pick up":
            load -= ITEM_WEIGHT[thing]
            cost += ITEM_WEIGHT[thing]
        elif action == "put down":
            load += ITEM_WEIGHT[thing]
        elif action == "unlock door to":
            cost += 1
    return cost

maxNodes = 1000000
TIME_LIMIT = int(5 * 60)
GOALS = [goal_1, goal_2, goal_3]

testCases = [   # breadth-first search
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":None,            "cost":None        },

                # depth-first search
                {"mode":"DF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":None,            "cost":None        }, 

                # Dijkstra (uniform cost) search
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":None,            "cost":weightedCost},

                # best-first (greedy) search
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":misplaced_items, "cost":None        }, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":minimum_trips,   "cost":None        }, 

                # A* search
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":misplaced_items, "cost":simpleCost  }, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":minimum_trips,   "cost":simpleCost  },
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":misplaced_items, "cost":weightedCost}, 
                {"mode":"BF", "max_nodes":maxNodes, "loop_check":True,  "randomise":False, "heuristic":minimum_trips,   "cost":weightedCost}
            ]

# function arguments to show less debug info on screen
kwargs = {"show_path":False, "show_state_path":False, "dots":True}

for x, GOAL in enumerate(GOALS):
    RW = RobotWorker(state, GOAL)
    goal_item_locations = GOAL
    print("\n**********RUNNING TEST CASES FOR GOAL STATE: ", x+1, "**********")

    for y, testArgs in enumerate(testCases):
        print("\n*****RUNNING TEST", y+1, "WITH ARGS:" , testArgs)
        signal.alarm(TIME_LIMIT)
        try:
            res = search(RW, **testArgs, **kwargs)["result"]
            print("Path Cost                      =     ", weightedCost(res["path"], res["goal_state"]))
        except:
            print("TIMEOUT")

print("\n\n******FINISHED******")
sys.stdout = orig_stdout
f.close()
print("\n\n******FINISHED******")
