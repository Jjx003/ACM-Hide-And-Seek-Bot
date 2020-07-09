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


# TODO: Create hidden blocks function

while True:

    commands = []
    units = agent.units # list of units you own
    opposingUnits = agent.opposingUnits # list of units on other team that you can see
    game_map = agent.map # the map
    round_num = agent.round_num # the round number

    if (agent.team == Team.SEEKER):
        # AI Code for seeker goes here
        commands = agent.do_seeking()
    else:
        commands = agent.do_hiding2()

    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()

    # wait for update from match engine
    agent.update()
