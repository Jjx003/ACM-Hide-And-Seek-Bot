import sys
import random 
import numpy as np
from datetime import datetime
from scipy.sparse.csgraph import floyd_warshall
from scipy.spatial import ConvexHull
from enum import Enum
from functools import cmp_to_key

random.seed(datetime.now())

# TODO: Make sure none of the island's peices are touching the edges
# Can do a for loop after the explore method (because it's non-intrusive)

directions = [(0,-1),(1,0),(0,1),(-1,0)]

def neighbors(i,j, maze):
    n = []
    rows = len(maze)
    cols = len(maze[0])
    for (dx, dy) in directions:
        px = j + dx
        py = i + dy
        if px >= 0 and px < cols and py >= 0 and py < rows and maze[py][px] == 1:
            n.append((py, px))
    return n

def explore(i,j, visited, maze):
    if (i, j) in visited:
        return None

    islands = [(i,j)]
    stack = [(i,j)]
    visited.add((i,j))
    
    while len(stack) > 0:
        cell = stack.pop()
        (cell_i, cell_j) = cell
        for neighbor in neighbors(cell_i, cell_j, maze):
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                islands.append(neighbor)

    return islands

class island_class():
    def __init__(self, points):
        self.points = points
        self.vertices = []
        self.volume = 0.0

    def set_vertices(self, v):
        self.vertices = v

    def set_volume(self, v):
        self.volume = v

    def get_volume(self):
        return self.volume

    def get_vertices(self):
        return self.vertices

    def __len__(self):
        return len(self.points)

    def __getitem__(self, position):
        return self.points[position]

    def __hash__(self):
        return hash(self.points[0]) # Just use hash of point[0] tupple



def all_islands(maze):
    components = []
    visited = set()
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                result = explore(i,j, visited, maze)
                if result != None:
                    components.append(island_class(result))
    
    valid = []
    for island in components:
        if len(island) >= 5:
            bad = False
            for (py,px) in island:
                if px == cols - 1 or py == rows - 1 or px == 0 or py == 0:
                    bad = True
                    break
            if not bad:
                valid.append(island)

    return valid

def outline(maze):
    outlines = []
    point_to_island = {}

    for island in all_islands(maze):
        marked = set()
        for (i, j) in island:
            for (dx, dy) in directions:
                op = (dy+i, dx+j)
                if op not in marked and maze[op[0]][op[1]] == 0:
                    marked.add(op)
                    point_to_island[op] = island
        outlines.append(list(marked))


    return (outlines, point_to_island)

def tupple_to_np(tups):
    result = []
    for (i,j) in tups:
        result.append([i,j])

    return np.array(result)

# Will return all the islands with their vertices, and outline points
def hull(maze):
    rows = len(maze)
    cols = len(maze[0])
    (outlines, point_to_island) = outline(maze)
    corner_to_island = {}
    islands = []

    for out in outlines:
        points = tupple_to_np(out)
        h = ConvexHull(points)
        v = []
        for corner_index in h.vertices:
            corner = out[corner_index]
            i = corner[0]
            j = corner[1]
            v.append((i, j))

        island = point_to_island[v[0]]
        island.set_vertices(v)
        island.set_volume(h.volume)
        islands.append(island)

    return islands

def closest_island(i,j, choices):
    closest = None
    recommended_point = None
    distance = 1 << 15
#    if random.randint(1,3) == 1:
    for island in choices:
        for corner in island.get_vertices():
            (ci, cj) = corner
            d = (i-ci)**2 + (j-cj)**2
            if d < distance:
                closest = island
                distance = d
                recommended_point = (ci, cj)
#    else:
#        points = []
#        weights = []
#
#        for island in choices:
#            closest_corner = 1 << 31
#            c = island.get_vertices()[0]
#            for corner in island.get_vertices():
#                (ci, cj) = corner
#                d = (i-ci)**2 + (j-cj)**2
#                if d < closest_corner:
#                    closest_corner = d
#                    c = corner
#
#            if closest_corner <= 0:
#                closest_corner = 1
#
#            weights.append(1+20/closest_corner+len(island))
#            points.append((c, island))
#
#        (recommended_point, closest) = random.choices(points, weights=weights)[0]
#        (ci, cj) = recommended_point
#        distance = (i-ci)**2 + (j-cj)**2


    return (closest, recommended_point, distance)

def apply_direction(x, y, dir):
    newx = x
    newy = y
    if (dir == 0):
        newy -= 1
    elif (dir == 1):
        newy -= 1
        newx += 1
    elif (dir == 2):
        newx += 1
    elif (dir ==3):
        newx += 1
        newy += 1
    elif (dir == 4):
        newy += 1
    elif (dir == 5):
        newy += 1
        newx -= 1
    elif (dir == 6):
        newx -= 1
    elif (dir == 7):
        newx -= 1
        newy -= 1
    elif (dir == 8):
        pass
    
    return (newx, newy)

def read_input():
    """
    Reads input from stdin
    """
    try:
        return input()
    except EOFError as eof:
        raise SystemExit(eof)

def distance_compare(a,b):
    if (a[0] > b[0]):
        return 1
    return -1
      
class Team(Enum):
    SEEKER = 2
    HIDER = 3

class Direction(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    STILL = 8

class Unit:
    def __init__(self, id, x, y, dist):
        self.id = id
        self.x = x
        self.y = y
        self.distance = dist
        self.state = None
        self.tasks = []
        self.dir = None
        self.last_pos = (-100,-100)
        self.offset = False
        self.clock = 1

    def setState(state):
        self.state = state

    def move(self, dir: int) -> str:
        return "%d_%d" % (self.id, dir)


class Agent:
    round_num = 0
    """
    Constructor for a new agent
    User should edit this according to their `Design`
    """
    def __init__(self):
        self.state = 'stall'
        self.target_id = None
        self.last_seen = None
        self.visited = set()
        self.map_set = set()
        self.remaining = set()
        self.islands = None

    def update_visited(self, x, y):
        for (i,j) in [(x,y),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x,y-1)]:
            if (i >=0 and i < self.width and j >= 0 and j < self.height and self.map[j][i] == 0):
                self.visited.add((i,j))
                pair = (i,j)
                if pair in self.remaining:
                    self.remaining.remove(pair)

    def get_random_offset3(self, origin_x, origin_y, radius):
        rx = random.randint(-radius,radius)
        ry = random.randint(-radius,radius)
        posx = origin_x + rx
        posy = origin_y + ry

        while posx < 0 or posx >= self.width or posy < 0 or posy >= self.height or (posx, posy) == (origin_x, origin_y) or self.map[posy][posx] != 0:

            rx = random.randint(-radius,radius)
            ry = random.randint(-radius,radius)
            posx = origin_x + rx
            posy = origin_y + ry
        ###print(f'New way point at {posx},{posy} with value', self.map[posy][posx], file=sys.stderr)
        return (posx, posy)

    def get_random_offset(self, origin_x, origin_y, radius):
        rx = random.randint(-radius,radius)
        ry = random.randint(-radius,radius)
        posx = origin_x + rx
        posy = origin_y + ry

        if (len(self.remaining) == 0):
            self.remaining = self.map_set.clone()

        chosen = random.choice(list(self.remaining))
        return chosen

        '''
        while posx < 0 or posx >= self.width or posy < 0 or posy >= self.height or (posx, posy) == (origin_x, origin_y) or self.map[posy][posx] != 0:

            rx = random.randint(-radius,radius)
            ry = random.randint(-radius,radius)
            posx = origin_x + rx
            posy = origin_y + ry
        ###print(f'New way point at {posx},{posy} with value', self.map[posy][posx], file=sys.stderr)
        '''
        #return (posx, posy)

    def get_random_offset2(self, origin_x, origin_y, choices):
        chosen = random.choice(list(choices))
        return chosen


    def do_bounce(self):
        self.state = 'bounce'
        for bot in self.units:
            bot.state = 'bouncing'
            if (bot.last_pos == (bot.x, bot.y)):
                bot.tasks = []
            bot.last_pos = (bot.x, bot.y)
            #bot.dir = random.choice(list(Direction)).value
            if len(bot.tasks) == 0:
                bot.tasks.append(self.get_random_offset(bot.x, bot.y, 10))
                #bot.tasks.append(

    def do_swarm(self, target):
        self.state = 'swarming'
        self.target_id = target.id
        self.last_seen = (target.x, target.y)
        for bot in self.units:
            bot.state = 'swarm'
            bot.tasks = []
            #if (random.randint(0, 1) == 0):
                #bot.tasks.append(self.get_random_offset(bot.x, bot.y, 5))

    def generate_path(self, bot, destination):
        path = []
        (dx, dy) = destination
        p1 = self.width * bot.y + bot.x
        p2 = self.width * dy + dx
        c = self.pred[p1, p2]
        ###print((dx,dy),self.width, self.height, 'are the constraints', file=sys.stderr)
        ###print('the distnace to your target is ', self.dist_matrix[p1, p2], file=sys.stderr)
        path.append(destination)

        while c != p1 and c >= 0:
            x = c % self.width
            y = c // self.width
            path.append((x,y))
            c = self.pred[p1, c]

        ###print(destination,'||', path, '||', (bot.x, bot.y), file=sys.stderr)

        return list(reversed(path))

    def check_tagged(self):
        pos = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        my_ids = set()
        for bot in self.units:
            my_ids.add(bot.id)

        for bot in self.units:
            for (i,j) in pos:
                x = bot.x + j
                y = bot.x + i
                if (y>=0 and y<self.height and x>=0 and x<self.width):
                    val = self.map[y][x]
                    if (val != 0 and val not in my_ids and val != 1):
                        if (val == self.target_id):
                            # Completed target task!
                            self.state = 'stall'
                            self.target_id = None
                            ###print('We tgged someone, clearing', file=sys.stderr)
                            break


    def do_tasks(self):
        commands = []
        moved = set()
        for bot in self.units:
            if (len(bot.tasks) > 0):
                # Do tasks first
                (tx, ty) = bot.tasks[0]
                self.update_visited(bot.x, bot.y)
                if (bot.x == tx and bot.y == ty):
                    del bot.tasks[0]
                    ###print('Goal was reached!', file=sys.stderr)
                else:
                    # Continue moving towards target
                    path = self.generate_path(bot, bot.tasks[0])
                    ###print(self.map[bot.y][bot.x],'is the bot pos value', self.map[bot.tasks[0][1]][bot.tasks[0][0]],'is desination value', file=sys.stderr)
                    (goalx, goaly) = bot.tasks[0]
                    ###print((goalx,goaly), (bot.x, bot.y), self.map[goaly][goalx], file=sys.stderr)
                    ###print(path[0], path[1], file=sys.stderr)
                    (pointx, pointy) = path[0]

                    ###print('what',path[1], path[-1], (bot.x,bot.y), file=sys.stderr)
                    ###print('what are you doing', (pointx, pointy), (bot.x, bot.y), file=sys.stderr)
                    # Reversed: positive y is going down
                    rdir = (pointx-bot.x, bot.y-pointy)
                    d = None
                    if (rdir == (-1,0)):
                        d = Direction.WEST
                    elif (rdir == (-1,1)):
                        d = Direction.NORTHWEST
                    elif (rdir == (0,1)):
                        d = Direction.NORTH
                    elif (rdir == (1,1)):
                        d = Direction.NORTHEAST
                    elif (rdir == (1,0)):
                        d = Direction.EAST
                    elif (rdir == (1,-1)):
                        d = Direction.SOUTHEAST
                    elif (rdir == (0,-1)):
                        d = Direction.SOUTH
                    elif (rdir == (-1,-1)):
                        d = Direction.SOUTHWEST
                    else:
                        continue
                    commands.append(bot.move(d.value))
                    moved.add(bot)


        # Then follow state behavior
        # TODO: Replace primitive chase
        target = None
        for hider in self.opposingUnits:
            if (hider.id == self.target_id):
                target = hider
                break

        if (target == None):
            # Suddenly disappeared D:
            # TODO: Use power of inference
            self.last_seen = None
            self.state = 'stall'
        else:
            # Target still in sight, move towards if no task
            self.state = 'swarming'
            ###print('should be moving as if i were swarming', file=sys.stderr)
            for bot in self.units:
                if (bot not in moved):
                    ###print('Thankfully I havent moved yet so lets do that', file=sys.stderr)
                    path = self.generate_path(bot, (target.x, target.y))
                    if (len(path) == 0):
                        pass
                        ##print('lenght to goal is 0?', (bot.x,bot.y),(target.x,target.y),file=sys.stderr)
                    else:
                        (pointx, pointy) = path[0]
                        rdir = (pointx-bot.x, bot.y-pointy)
                        d = None

                        if (rdir == (-1,0)):
                            d = Direction.WEST
                        elif (rdir == (-1,1)):
                            d = Direction.NORTHWEST
                        elif (rdir == (0,1)):
                            d = Direction.NORTH
                        elif (rdir == (1,1)):
                            d = Direction.NORTHEAST
                        elif (rdir == (1,0)):
                            d = Direction.EAST
                        elif (rdir == (1,-1)):
                            d = Direction.SOUTHEAST
                        elif (rdir == (0,-1)):
                            d = Direction.SOUTH
                        elif (rdir == (-1,-1)):
                            d = Direction.SOUTHWEST
                        else:
                            pass
 
                        ###print('appending command to move towards the idiot', (bot.x,bot.y),(target.x,target.y),file=sys.stderr)
                        commands.append(bot.move(d.value))

        return commands

    def eval_state(self):
        if (self.state == 'stall' or self.state == 'bounce'):
            choices = []
            for v in self.opposingUnits:
                combined_distance = 0
                for v2 in self.units:
                    p1 = v.y * self.width + v.x
                    p2 = v2.y * self.width + v2.x
                    combined_distance += self.dist_matrix[p1, p2]
                    # Use floyd warshall
                choices.append((combined_distance, v))

            if (len(choices) > 0):
                # Perform swarm
                choices = sorted(choices, key=cmp_to_key(distance_compare))
                closest = choices[0][1]
                self.do_swarm(closest)
            else:
                # Perform bounce
                self.do_bounce()
        elif (self.state == 'swarming'):
            # Idea: If opposing unit suddenly disappears, the more units you have,
            # the less blind spots will occur. Aggregate all blind spots into a set.
            # Check all positions (8) that are valid if they hit the blind spot location.
            # If two bots: send one to converge on blind spot furthest away (try go get them to come from different directions)
            # If three: send two to converge and third to explore random one as an explorer

            # TODO: Replace primitive chase
            target = None
            for hider in self.opposingUnits:
                if (hider.id == self.target_id):
                    target = hider
                    break

            if (target == None):
                # Suddenly disappeared D:
                for bot in self.units:
                    bot.tasks = [self.last_seen]
                
                self.last_seen = None
                # TODO: Use power of inference and replace this dumb logic
                #self.do_bounce()
                #self.last_seen = None
            else:
                #self.do_swarm(target)
                pass
                

    def do_seeking(self):
        """
        Manages Agent's units under the assumption that we are the seekers
        """
        # Idea: Create state for agent based on closest enemy.
        # Send all units to swarm this one person until completion.
        self.eval_state()
        commands = self.do_tasks()
        self.check_tagged()
        return commands


    def check_path(self, path, bad):
        for p in path:
            if p in bad:
                return False
        return True

    def check_bad_end(self, endPos):
        dirs = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        (x,y) = endPos
        if (x+1 == self.width or y+1 == self.height or x == 0 or y == 0):
            return True 
        visited = set()
        stack = [((x,y),0)]
        good_volume = 8
        max_d = 8
        while len(stack) > 0:
            if (len(visited) >= good_volume):
                return False 
            ((px, py), d) = stack.pop()
            for (i,j) in dirs:
                po = (px+i, py+j)
                if (self.check_pos(px+i,py+j) and self.map[py+j][px+i] == 0) and po not in visited:
                    visited.add(po)
                    if (d < max_d):
                        stack.append(((px+i, py+j), d+1))

        return len(visited) < good_volume 
                    

    def minimax(self, state, depth):
        dirs = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        if (depth == 4 and state == 'hide'):
            pass

    def mxHider(self):
        hiders = []
        seekers = []
        for bot in self.units:
            hiders.append((bot.x, bot.y))

        for enemy in self.opposingUnits:
            seekers.append((enemy.x, enemy.y))

        (move, score) = self.minimax('hide', 0)


    def execute_move(self, bot, next_pos):
        (goalx, goaly) = next_pos
        rdir = (goalx-bot.x, bot.y-goaly)
        d = None

        if (rdir == (-1,0)):
            d = Direction.WEST
        elif (rdir == (-1,1)):
            d = Direction.NORTHWEST
        elif (rdir == (0,1)):
            d = Direction.NORTH
        elif (rdir == (1,1)):
            d = Direction.NORTHEAST
        elif (rdir == (1,0)):
            d = Direction.EAST
        elif (rdir == (1,-1)):
            d = Direction.SOUTHEAST
        elif (rdir == (0,-1)):
            d = Direction.SOUTH
        elif (rdir == (-1,-1)):
            d = Direction.SOUTHWEST
        else:
            ##print('why bruh', rdir, file=sys.stderr)
            poss = []
            dirs = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
            for (x,y) in dirs:
                np = (bot.x+x, bot.y+y)
                if (self.check_pos(np[0], np[1]) and self.map[np[1]][np[0]] == 0):
                    p = True 
                    for e in self.opposingUnits:
                        if ((e.x-np[0])^2 + (e.y-np[1])^2 <= bot.distance):
                            p = False
                            break
                    if (p):
                        poss.append(np)
            if (len(poss) > 0):
                return self.execute_move(bot, random.choice(poss)) 
            else:
                return None

        return bot.move(d.value)

    def check_pos(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def check_bad_hiding(self, pos):
        # 4x4 check
        (x, y) = pos
        value = False
        # X0
        # 0X
        if ((self.check_pos(x+1, y-1) and self.map[y-1][x] != 0 and self.map[y][x+1] != 0) or
                (self.check_pos(x-1,y+1) and self.map[y][x-1] != 0 and self.map[y+1][x] != 0)):
            return True
        # 0X
        # X0
        elif ((self.check_pos(x+1,y+1) and self.map[y][x+1] != 0 and self.map[y-1][x] != 0) or
                (self.check_pos(x-1, y-1) and self.map[y][x-1] != 0 and self.map[y-1][x] != 0 )):
            return True
        elif (self.check_pos(x+1,y+1) and self.check_pos(x-1, y-1)):
            bad_score = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if (self.map[y+i][x+j] == 0):
                        bad_score += 1
                if (bad_score >= 6):
                    return True
                else:
                    return random.randint(0,bad_score) > 2
        return False



    def do_hiding2(self):
        #if self.round_num == 0:
        #    return []
        if not self.islands:

            self.islands = hull(self.map)
            self.waypoints = set()
            ##print('what is happening', self.islands, file=sys.stderr)
            if len(self.islands) == 0:
                return self.do_hiding()

        commands = []
        choices = set(self.islands)
        

        if self.state == 'stall':
            for bot in self.units:
                (closest, recommended_point, distance) = closest_island(bot.y, bot.x, choices)
                vertex_index = 0
                if recommended_point in self.waypoints:
                    for i, point in enumerate(closest.get_vertices()):
                        if point not in self.waypoints:
                            recommended_point = point
                            vertex_index = i
                            break
                else:
                    for i, point in enumerate(closest.get_vertices()):
                        if point == recommended_point:
                            vertex_index = i
                            break

                (y, x) = recommended_point
                self.waypoints.add(recommended_point)
                bot.tasks = [(x,y)]
                bot.state = 'zoom'
                bot.index = vertex_index
                bot.current_island = closest

            self.state = ''
            self.waypoints = set()
        else:
            for bot in self.units:

                if len(bot.tasks) > 0 or bot.state == 'zoom':
                    task = bot.tasks[0]
                    if (bot.x, bot.y) == task:
                        ##print('we reached the task', file=sys.stderr)
                        del bot.tasks[0]
                        bot.state = 'latched'
                        #if not bot.offset or self.check_bad_hiding((bot.x, bot.y)):
                        #    print('task assigned becasue bad position', file=sys.stderr)
                        #    bot.offset = True
                        #    choice1 = (bot.index + bot.clock) % len(bot.current_island.get_vertices())
                        #    (y, x) = bot.current_island.get_vertices()[choice1]
                        #    path = self.generate_path(bot, (x, y))
                        #    (x1,y1) = path[random.randint(0, len(path)-1)]
                        #    if (x1,y1) == (bot.x, bot.y):
                        #        print('Already on, move!', file=sys.stderr)
                        #        bot.index = choice1
                        #        bot.task = [(x,y)]
                        #    else:
                        #        print('ok to proceed step!', file=sys.stderr)
                        #        bot.task = [(x1,y1)]
                        #else:
                        #    bot.offset = False

                if len(self.opposingUnits) > 0:
                    # Move to the next waypoint

                    closest_enemy = self.opposingUnits[0]
                    d = self.dist_matrix[closest_enemy.y*self.width + closest_enemy.x, bot.y*self.width + bot.x]

                    for enemy in self.opposingUnits:
                        p1 = bot.y*self.width + bot.x
                        p2 = enemy.y*self.width + enemy.x
                        nd = self.dist_matrix[p1, p2]
                        if nd < d:
                            closest_enemy = enemy
                            d = nd

                    enemy = closest_enemy
                    ##print('RUNNNN', file=sys.stderr)

                    p1 = bot.y*self.width + bot.x
                    p2 = enemy.y*self.width + enemy.x

                    ticker = 1
                    if bot.current_island.get_volume() > 5:
                        ticker = 1+random.randint(0,1)

                    choice1 = (bot.index + ticker) % len(bot.current_island.get_vertices())
                    choice2 = (bot.index - ticker) % len(bot.current_island.get_vertices())
                    (y, x) = bot.current_island.get_vertices()[choice1]
                    (y2, x2) = bot.current_island.get_vertices()[choice2]
                    p3 = y*self.width + x
                    p4 = y2*self.width + x2

                    ##print('choice1 distance', self.dist_matrix[p3, p2], 'current di', self.dist_matrix[p1, p2], file=sys.stderr)
                    ##print('choice2 distance', self.dist_matrix[p4, p2], 'current di', self.dist_matrix[p1, p2], file=sys.stderr)
                    (ax, ay) = self.generate_path(bot, (x,y))[0]
                    (bx, by) = self.generate_path(bot, (x2,y2))[0]

                    path1p = ay*self.width + ax
                    path2p = by*self.width + bx

                    #print('task assinged because we see enemy', file=sys.stderr)
                    
                    #if self.dist_matrix[path1p, p2] > self.dist_matrix[path2p, p2]:
                    if (enemy.y-ay)**2 + (enemy.x-ax)**2 > (enemy.y-by)**2 + (enemy.x-bx)**2:
                        ##print('we are doing choice1',file=sys.stderr)
                        bot.index = choice1
                        bot.tasks = [(x,y)]
                        bot.clock = 1
                    else:
                        ##print('we are doing choice2',file=sys.stderr)
                        bot.index = choice2
                        bot.tasks = [(x2,y2)]
                        bot.clock = -1

    

        for bot in self.units:
            if len(bot.tasks) > 0:
                #print('tasked:', bot.tasks[0], file=sys.stderr)
                #print('current', bot.x, bot.y, file=sys.stderr)
                path = self.generate_path(bot, bot.tasks[0])
                #print(path, file=sys.stderr)
                step = path[0]
                move = self.execute_move(bot, step)
                if move != None:
                    commands.append(move)
                else:
                    pass
                    print('why are you not move', file=sys.stderr)
            else:
                pass
                ##print('what do', file=sys.stderr)

        return commands





    def do_hiding(self):
        commands = []
        seen = []
        if (len(self.opposingUnits) > 0):
            choices = self.map_set.copy() 
            bad = set()
            for enemy in self.opposingUnits:
                stack = [((enemy.x, enemy.y),0)]
                dirs = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
                seen.append((enemy.x, enemy.y))
                visited = set()
                while len(stack) > 0:
                    ((x,y), distance) = stack.pop()
                    pos = (x,y)
                    bad.add(pos)
                    if (pos in choices):
                        choices.remove(pos)
                    if (distance < 2):
                        for (dx, dy) in dirs:
                            (posx, posy) = (x+dx, y+dy)
                            if (posx >= 0 and posx < self.width and posy >= 0 and posy < self.height and self.map[posy][posx] == 0 and (posx,posy) not in visited):
                                visited.add((posx,posy))
                                stack.append(((posx, posy), distance + 1))

            self.last_seen = seen

            for bot in self.units:
                

                if (bot.distance > 0):
                    # We are compromised
                    (x,y) = (bot.x, bot.y)
                    #choices2 = set([(x,y),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x,y-1)])

                    tries = 0
                    #path = self.generate_path(bot, self.get_random_offset2(bot.x, bot.y, choices))
                    #path = self.generate_path(bot, self.get_random_offset2(bot.x, bot.y, choices2))
                    path = self.generate_path(bot, self.get_random_offset3(bot.x, bot.y, 12))
                    ok_path = path
                    #while tries <= 300 and not self.check_path(path, bad):
                    while tries <= 200 and not self.check_path(path, bad) and not self.check_bad_hiding(path[-1]) and not self.check_bad_end(path[-1]):
                    #while len(choices) > 0 and not self.check_path(path, bad):
                        tries += 1
                        #path = self.generate_path(bot, self.get_random_offset2(bot.x, bot.y, choices))
                        path = self.generate_path(bot, self.get_random_offset3(bot.x, bot.y, 5))
                        if (path[0] in choices):
                            choices.remove(path[0])
                        if (path[-1] in choices):
                            choices.remove(path[-1])
                        if (len(path) > 0):
                            ok_path = path

                    (goalx, goaly) = (None, None)


                    if (len(path) > 0):
                        (goalx, goaly) = path[0]
                        bot.tasks = [path[-1]]
                    elif (len(ok_path) > 0):
                        (goalx, goaly) = ok_path[0]
                        bot.tasks = [ok_path[-1]]

                    if (goalx, goaly) != (None, None):
                        # Make move
                        ##print('run away! current|goal', (bot.x,bot.y),'|',bot.tasks[0], file=sys.stderr)
                        move  = self.execute_move(bot, (goalx,goaly))
 
                        if (move != None):
                            commands.append(move)
                        else:
                            pass

                                                

                    else:
                        pass
                        ##print('guess we dead', file=sys.stderr)
                else:
                    if (len(bot.tasks) > 0):
                        if ((bot.x, bot.y) == bot.tasks[0]):
                            del bot.tasks[0]
                            ##print('task completed :)',file=sys.stderr)
                        else:
                            ##print('not reached yet, current|goal', (bot.x,bot.y),'|',bot.tasks[0], file=sys.stderr)
                            path = self.generate_path(bot, bot.tasks[0]) 
                            move = self.execute_move(bot, path[0])
                            ##print('path idea?', path, file=sys.stderr)
                            if (move != None):
                                ##print('until completion comrades!', file=sys.stderr)
                                commands.append(move)
                            else:
                                pass
                                ##print('why none??', file=sys.stderr)

        else:
            choices = self.map_set.copy() 
            bad = set()
            if (self.last_seen):
                for (x,y) in self.last_seen:
                    stack = [((x, y),0)]
                    dirs = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
                    while len(stack) > 0:
                        ((x,y), distance) = stack.pop()
                        pos = (x,y)
                        bad.add(pos)
                        if (pos in choices):
                            choices.remove(pos)
                        if (distance < 3):
                            for (dx, dy) in dirs:
                                (posx, posy) = (x+dx, y+dy)
                                if (posx >= 0 and posx < self.width and posy >= 0 and posy < self.height and self.map[posy][posx] == 0):
                                    stack.append(((posx, posy), distance + 1))

            ##print('not spotted rn', file=sys.stderr)
            for bot in self.units:
                if (len(bot.tasks) > 0):
                    if ((bot.x, bot.y) == bot.tasks[0]):
                        del bot.tasks[0]
                        ##print('task completed :)',file=sys.stderr)
                    else:
                        ##print('not reached yet, current|goal', (bot.x,bot.y),'|',bot.tasks[0], file=sys.stderr)
                        path = self.generate_path(bot, bot.tasks[0]) 
                        move = self.execute_move(bot, path[0])
                        p1 = bot.y*self.width + bot.x
                        p2 = bot.tasks[0][1]*self.width + bot.tasks[0][0]
                        ##print('path idea?', path,self.dist_matrix[p1,p2], file=sys.stderr)
                        if (move != None):
                            ##print('until completion comrades!', file=sys.stderr)
                            commands.append(move)
                        else:
                            pass
                            ##print('why none??', file=sys.stderr)
                else:
                    if (self.check_bad_hiding((bot.x, bot.y) or random.randint(1,50)==3)):
                        ##print('section 2', file=sys.stderr)
                        tries = 0
                        path = self.generate_path(bot, self.get_random_offset3(bot.x, bot.y, 10))
                        #while tries <= 300 and not self.check_path(path, bad):
                        while tries <= 100 and not self.check_bad_hiding(path[-1]) and not self.check_path(path, bad) and not self.check_bad_end(path[-1]):
                        #while len(choices) > 0 and not self.check_path(path, bad):
                            tries += 1
                            #path = self.generate_path(bot, self.get_random_offset2(bot.x, bot.y, choices))
                            path = self.generate_path(bot, self.get_random_offset3(bot.x, bot.y, 8))

                        (goalx, goaly) = (None, None)

                        if (len(path) > 0):
                            (goalx, goaly) = path[0]
                            bot.tasks.append(path[-1])

                        self.execute_move(bot, (goalx, goaly))




        return commands


    """
    Initialize Agent for the `Match`
    User should edit this according to their `Design`
    """
    def initialize(self):
        meta = read_input().split(",")
        self.id = int(meta[0])
        self.team = Team(int(meta[1]))

        self.units = []
        self.unitsDict = {}
        self._store_unit_info()
        [width, height] = [int(i) for i in (read_input().split(","))]

        self.matrix = np.zeros((width*height, width*height))
        self.height = height
        self.width = width
        self.map = []

        for i in range(height):
            line = read_input().split(",")
            parsedList = []
            for j in range(len(line)):
                if line[j] != '':
                    origin = int(line[j])
                    parsedList.append(origin)

            self.map.append(parsedList)

        # j is row(y)
        # i is col(x)

        for j in range(height):
            for i in range(width):
                if (self.map[j][i] == 0):
                    self.map_set.add((i,j))
                    # current point (i,j)
                    for (x,y) in [(i-1,j),(i-1,j-1),(i,j-1),(i+1,j-1)]:
                        # Make sure within bounds
                        if x >= 0 and x < width and y >= 0 and y < height and self.map[y][x] == 0:
                            p1 = j*self.width + i
                            p2 = y*self.width + x

                            if (x,y) == (i-1, j-1) or (x,y) == (i+1, j-1):
                                self.matrix[p1, p2] = 1.414
                                self.matrix[p2, p1] = 1.414
                            else:
                                self.matrix[p1, p2] = 1
                                self.matrix[p2, p1] = 1 

        dist_matrix, pred = floyd_warshall(self.matrix, directed=False, return_predecessors=True)
        self.dist_matrix = dist_matrix
        self.pred = pred
        self.remaining = self.map_set.copy()

        self.round_num = 0
        self._update_map_with_ids()

    def _reset_map(self):

        for _, unit in enumerate(self.units):
            self.map[unit.y][unit.x] = 0

        for _, unit in enumerate(self.opposingUnits):
            self.map[unit.y][unit.x] = 0

    def _update_map_with_ids(self):

         # add unit ids to map
        for _, unit in enumerate(self.units):
            self.map[unit.y][unit.x] = unit.id
        
        # add unit ids to map
        for _, unit in enumerate(self.opposingUnits):
            self.map[unit.y][unit.x] = unit.id

    def _store_unit_info(self):
        units_and_coords = read_input().split(",")
        new_list = []
        mentioned = set()

        for _, val in enumerate(units_and_coords):
            if (val != ""):
                [id, x, y, dist] = [int(k) for k in val.split("_")]
                if (len(self.units) == 0):
                    new_unit = Unit(id, x, y, dist)
                    new_list.append(new_unit)
                    self.unitsDict[str(id)] = new_unit
                else:
                    current_unit = self.unitsDict[str(id)]
                    current_unit.x = x
                    current_unit.y = y
                    current_unit.dist = dist
                    mentioned.add(id)

        # Takes account of bots that "died"
        for bot in self.units:
            if (bot.id in mentioned):
                new_list.append(bot)

        if len(new_list) > 0:
            self.units = new_list


        units_and_coords = read_input().split(",")

        self.opposingUnits = []
        for _, value in enumerate(units_and_coords):
            if (value != ""):
                [id, x, y] = [int(k) for k in value.split("_")]
                self.opposingUnits.append(Unit(id, x, y, -1))


    """
    Updates Agent's own known state of `Match`
    User should edit this according to their `Design
    """
    def update(self):
        self.round_num += 1
        self._reset_map()
        self._store_unit_info()
        self._update_map_with_ids()

    """
    End a turn
    """
    def end_turn(self):
        print('D_FINISH')
        
