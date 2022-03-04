from bbmodcache.bbSearch import SearchProblem
from copy import deepcopy

ITEM_WEIGHT = {
      'rusty key' : 1,
         'bucket' : 2,
       'suitcase' : 4,
    'screwdriver' : 1,
  'sledge hammer' : 5,
          'anvil' : 12,
       'backpack' : 4,
        'keycard' : 2,
       'iron key' : 3
}

class Robot:
    def __init__(self, location, carried_items, strength):
        self.location      = location
        self.carried_items = carried_items
        self.strength      = strength
        
    def weight_carried(self):
        return sum([ITEM_WEIGHT[i] for i in self.carried_items])
    
    ## Define unique string representation for the state of the robot object
    def __repr__(self):
        return str( ( self.location, 
                      self.carried_items,
                      self.strength ) )
            
class Door:
    def __init__(self, roomA, roomB, doorkey=None, locked=False):
        self.goes_between = {roomA, roomB}
        self.doorkey      = doorkey
        self.locked       = locked
        # Define handy dictionary to get room on other side of a door
        self.other_loc = {roomA:roomB, roomB:roomA}
        
    ## Define a unique string representation for a door object    
    def __repr__(self):
        return str( ("door", self.goes_between, self.doorkey, self.locked) )


class State:
    def __init__( self, robot, doors, room_contents ):
        self.robot = robot
        self.doors = doors
        self.room_contents = room_contents
        
    ## Define a string representation that will be uniquely identify the state.
    ## An easy way is to form a tuple of representations of the components of 
    ## the state, then form a string from that:
    def __repr__(self):
        return str( ( self.robot.__repr__(),
                      [d.__repr__() for d in self.doors],
                      self.room_contents ) )


class RobotWorker(SearchProblem):
    def __init__(self, state, goal_item_locations):
        self.initial_state = state
        self.goal_item_locations = goal_item_locations

    def possible_actions(self, state):
        robot_location = state.robot.location
        strength = state.robot.strength
        weight_carried = state.robot.weight_carried()
        items = state.robot.carried_items
        actions = []
        # Can put down any carried item
        for i in state.robot.carried_items:
            actions.append(("put down", i))
        # Can pick up any item in room if strong enough
        for i in state.room_contents[robot_location]:
            if strength >= weight_carried + ITEM_WEIGHT[i]:
                actions.append(("pick up", i))
        # If there is an unlocked door between robot location and
        # another location can move to that location
        for door in state.doors:
            if robot_location not in door.goes_between:
                continue
            if door.locked == False:
                actions.append(("move to", door.other_loc[robot_location]))
            elif door.locked == True and door.doorkey in items:
                actions.append(
                    ("unlock door to", door.other_loc[robot_location]))
        # Now the actions list should contain all possible actions
        return actions

    def successor(self, state, action):
        next_state = deepcopy(state)
        act, target = action
        if act == "put down":
            next_state.robot.carried_items.remove(target)
            next_state.room_contents[state.robot.location].add(target)
        elif act == "pick up":
            next_state.robot.carried_items.append(target)
            next_state.room_contents[state.robot.location].remove(target)
        elif act == "move to":
            next_state.robot.location = target
        elif act == "unlock door to":
            robot_loc = next_state.robot.location
            for door in next_state.doors:
                if not door.locked:
                    continue
                connects = door.goes_between
                if robot_loc in connects and target in connects:
                    door.locked = False
                    break
        return next_state
        
    def goal_test(self, state):
        # print(state.room_contents)
        for room, contents in self.goal_item_locations.items():
            for i in contents:
                if not i in state.room_contents[room]:
                    return False
        return True

    def display_state(self, state):
        print("Robot location:", state.robot.location)
        print("Robot carrying:", state.robot.carried_items)
        print("Room contents:", state.room_contents)
