# Imports
from room import Room
from player import Player
from world import World

import random
from ast import Str, literal_eval

import collections
import random

############################################################
####################### STARTER CODE #######################
############################################################

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
player.current_room = world.starting_room
###________________________________________________________________________________________###

#######################################################################################
################################### HELPER FUNCTIONS ##################################
#######################################################################################
def new_room_for_map(room):
    '''
    Helper function to check if the room has been visited/mapped 
    already, and if not; add it and get the possible directions someone 
    can go.
    '''
    if room not in room_map:
        room_map[room] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}

        exits = room.get_exits()

        for direction in room_map[room]:
            if direction not in exits:
                room_map[room][direction] = 'NONE'
    
        return True
    else:
        return False

def add_room_relationships(starting_room, direction, ending_room):
    """
    basically once you have the room on the map, 
    you need to find its relationship to other rooms.
    """
    room_map[starting_room][direction] = ending_room
    room_map[ending_room][inverse[direction]] = starting_room

def path_to_closest_unexplored_exits(starting_room):
    """
    This function was a little weirder. Basically as long as the 
    path queue isnt empty, make sure the current room is added to 
    the 'visited' set if it isnt there already. If it is, just continue. 
    Then, still while not empty, it will loop through the 
    exit_directions for the current room, returning the path if 
    the direction hasnt been tried('?').Otherwise, copy that path to
    the 'new_path', append the exit directions to it, then instantiate new_room, 
    then append the path and room to the path_queue.
    This results in a clean list with the path to unexplored exits
    """
    visited = set()
    path_queue = collections.deque()

    path_queue.append((starting_room, []))

    while len(path_queue) > 0:
        room, path = path_queue.popleft()

        if room in visited:
            continue
        else:
            visited.add(room)

        for exit_direction in room_map[room]:
            if room_map[room][exit_direction] == '?':
                return path
            elif room_map[room][exit_direction] != 'NONE':
                new_path = path.copy()
                new_path.append(exit_direction)
                new_room = room_map[room][exit_direction]
                path_queue.append((new_room, new_path))
            
    return []
###___________________________________________________________________________________###

##############################################################################
############################### TRAVERSING ###################################
##############################################################################

traversal_path = [] # starter code

prevailing_direction = 's' 

change_direction = {'n': 'e', 'e': 's', 's': 'w', 'w': 'n'} # make dict for changing directions
inverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}  # make dict for opposite directions

room_map = {} # make empty dict for the map

new_room_for_map(player.current_room) # use helper function to add your current room to map, similar to adding to visited in past assignments

while len(room_map) < len(room_graph): # while we've not ben through every room:
    room = player.current_room # set current room
    exits = room.get_exits()# get exits
        
    found_unexplored_exit = False # default to false, so i can change later when they are found

    direction = prevailing_direction
    
    for num in range(len(change_direction)): # for every direction
        if room_map[room][direction] == '?' and direction in exits: # if the direction exists and is unexplored
            found_unexplored_exit = True # flag that i found an unexplored exit
            player.travel(direction) # then i can travel that direction
            next_room = player.current_room  # once im in the next room, have to set it as such
            traversal_path.append(direction) # add the direction to Traversal path

            
            if not new_room_for_map(next_room): # if we've already visited this room, backtrack, and take it off the traversal path
                player.travel(inverse[direction])
                traversal_path.pop()

            add_room_relationships(room, direction, next_room) # use helper function to make sure the map knows the relationship between current and next/last room
            break
        else:
            direction = change_direction[direction] # if this wasnt a good path, just change to go south


    if not found_unexplored_exit: # if no unexplored exit was found
        path = path_to_closest_unexplored_exits(room) # set the path to whatever is the closest room with unexplored exits

        traversal_path.extend(path) # then basically add that path to the traversal path
        for direction in path: # for each direction
            player.travel(direction) # follow it!
###__________________________________________________________________###

###########################################################
################## TRAVERSAL TEST CODE ####################
###########################################################
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")