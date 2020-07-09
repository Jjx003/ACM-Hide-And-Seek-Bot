from kit import Agent, Team, Direction, apply_direction
import math
import random 
import sys
import numpy as np
import copy


def e_print(*argv):
    print(*argv, file=sys.stderr)

# Create new agent
agent = Agent()
# initialize agent
agent.initialize()

'''
c = pred[p,p2]
e_print((agent.width, agent.height))
e_print(c)

limit = 50
count = 0
e_print((rx,ry),(rx2,ry2))
e_print(agent.map[ry][rx],agent.map[ry2][rx2],'are the values')
mat[ry2][rx2]='S'

x=None
y=None


while count < limit:
    count += 1
    e_print(c, 'is the c')

    x = c % agent.width
    y = c // agent.width

    e_print('path:', (x,y))
    mat[y][x] = 'X'
    c = pred[p,c]
    if c == p:
        mat[y][x]='E'
        break
'''

# TODO: Create hidden blocks function

while True:

    commands = []
    units = agent.units # list of units you own
    opposingUnits = agent.opposingUnits # list of units on other team that you can see
    game_map = agent.map # the map
    round_num = agent.round_num # the round number


    #print("testing 1,2,3", file=sys.stderr)
    
    if (agent.team == Team.SEEKER):
        # AI Code for seeker goes here
        commands = agent.do_seeking()
        #print(commands, 'are the move commands dude', file=sys.stderr)
        #print(round_num, 'IS ROUND', file=sys.stderr)
        '''  
        for _, unit in enumerate(units):
            # unit.id is id of the unit
            # unit.x unit.y are its coordinates, unit.distance is distance away from nearest opponent
            # game_map is the 2D map of what you can see. 
            # game_map[i][j] returns whats on that tile, 0 = empty, 1 = wall, 
            # anything else is then the id of a unit which can be yours or the opponents
        
             # choose a random direction to move in
            randomDirection = random.choice(list(Direction)).value
            #print(unit.x,unit.y, file=sys.stderr)
            
            # apply direction to current unit's position to check if that new position is on the game map            
            (x, y) = apply_direction(unit.x, unit.y, randomDirection)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(randomDirection))
        '''
        pass

    else:
        '''
        for _, unit in enumerate(units):
            randomDirection = random.choice(list(Direction)).value
            (x, y) = apply_direction(unit.x, unit.y, randomDirection)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(randomDirection))
        pass
        '''
        #if random.randint(1,25) == 3:
        commands = agent.do_hiding2()
        #else:
        #   commands = agent.do_hiding()




    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()

    # wait for update from match engine
    agent.update()
