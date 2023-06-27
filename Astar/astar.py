import display

nodes = []
running = False

start_node = None
end_node = None

open_positions = []
closed_positions = []
path = []

class Node:
    tile: display.Tile

    walkable: bool
    position : tuple

    parent = None

    gcost = 0
    hcost= 0

    def __init__(self, tile: display.Tile):
        self.tile = tile
        self.position = ((tile.position[0] -5)/20, (tile.position[1] -55)/20)
        self.walkable = tile.walkable

        if tile == display.start_tile:
            global start_node
            start_node = self
            print(self.position)

        if tile == display.end_tile:
            global end_node
            end_node = self

    def get_fcost(self):
        return self.gcost + self.hcost
    
    def get_neighbours(self):
        global nodes
        neighbours = []
        x = -1
        while x<=1:
            y = -1
            while y <=1:
                if x == 0 and y == 0:
                    y+=1
                    continue
                
                checkX = self.position[0] + x
                checkY = self.position[1] + y

                if checkX >=1 and checkX <= display.screen_bounds[0] and checkY >= 1 and checkY <= display.screen_bounds[1]:
                    neighbours.append(nodes[int(checkX-1 + (checkY-1) * display.screen_bounds[1])])
                
                y+=1
            x+=1

        
        x = self.position[0] 
        y = self.position[1] 
        topleft = (x-1, y-1)
        topright = (x+1, y-1)
        bottomleft = (x-1, y+1)
        bottomright = (x+1, y+1)
        for neighbour in neighbours:
            if neighbour.position == topleft:
                corner_walkable = nodes[int(x-1 + (y-2) * display.screen_bounds[1])].walkable or nodes[int(x-2 + (y-1) * display.screen_bounds[1])].walkable
                if not corner_walkable:
                    neighbours.remove(neighbour)

            if neighbour.position == topright:
                corner_walkable = nodes[int(x-1 + (y-2) * display.screen_bounds[1])].walkable or nodes[int(x + (y-1) * display.screen_bounds[1])].walkable
                if not corner_walkable:
                    neighbours.remove(neighbour)

            if neighbour.position == bottomleft:
                corner_walkable = nodes[int(x-2 + (y-1) * display.screen_bounds[1])].walkable or nodes[int(x-1 + (y) * display.screen_bounds[1])].walkable
                if not corner_walkable:
                    neighbours.remove(neighbour)

            if neighbour.position == bottomright:
                corner_walkable = nodes[int(x-1 + (y) * display.screen_bounds[1])].walkable or nodes[int(x + (y-1) * display.screen_bounds[1])].walkable
                if not corner_walkable:
                    neighbours.remove(neighbour)
        return neighbours 
    


def init():
    reset()
    for x, tile in enumerate(display.tiles):
        nodes.append(Node(tile))
        #print(nodes[x].position)
    if start_node and end_node:
        global running
        running = True
    else:
        print('please select start and end points')
        return

    open_positions.append(start_node)
    get_distance(start_node, end_node)

def abort():
    global running
    running = False
    print("end")

def find_path():
    if start_node and end_node:
        global running
        running = True
    else:
        print('please select start and end points')
        return
    
    while open_positions.__len__() > 0:
        current_node = open_positions[0]
        for node in open_positions:
            if node.get_fcost() < current_node.get_fcost():
                current_node = node

            if node.get_fcost() == current_node.get_fcost() and node.hcost < current_node.hcost:
                current_node = node

        open_positions.remove(current_node)
        closed_positions.append(current_node)

        if current_node == end_node:
            retrace_path()
            break
        neighbours = current_node.get_neighbours()

        for neighbour in neighbours:
            if not neighbour.walkable or closed_positions.__contains__(neighbour):
                continue

            new_movement_cost_to_neighbour = current_node.gcost + get_distance(current_node, neighbour)
            if new_movement_cost_to_neighbour < neighbour.gcost or not open_positions.__contains__(neighbour):
                neighbour.gcost = new_movement_cost_to_neighbour
                neighbour.hcost = get_distance(neighbour, end_node)
                neighbour.parent = current_node

                if not open_positions.__contains__(neighbour):
                    open_positions.append(neighbour)



def get_distance(nodeA: Node, nodeB: Node):
    distanceX = abs(nodeA.position[0] - nodeB.position[0])
    distanceY = abs(nodeA.position[1] - nodeB.position[1])
    
    if distanceX > distanceY: 
        return 14 * distanceY + 10 * (distanceX-distanceY)
    return 14 * distanceX + 10 * (distanceY-distanceX)

def retrace_path():
    global end_node
    global start_node
    global path
    current_node = end_node 
    while current_node != start_node:
        path.append(current_node)
        current_node = current_node.parent


    path.reverse()
    for node in path:
        if node != end_node:
            node.tile.set_state("path")

    abort()


def step_one_forward():
    if start_node and end_node:
        global running
        running = True
    else:
        print('please select start and end points')
        return
    
    if open_positions.__len__() > 0:
        current_node = open_positions[0]
        for node in open_positions:
            if node.get_fcost() < current_node.get_fcost():
                current_node = node

            if node.get_fcost() == current_node.get_fcost() and node.hcost < current_node.hcost:
                current_node = node

        open_positions.remove(current_node)
        closed_positions.append(current_node)
        if current_node != start_node and current_node != end_node:
            current_node.tile.set_state("closed")

        if current_node == end_node:
            retrace_path()
            return
        neighbours = current_node.get_neighbours()

        for neighbour in neighbours:
            if not neighbour.walkable or closed_positions.__contains__(neighbour):
                continue

            new_movement_cost_to_neighbour = current_node.gcost + get_distance(current_node, neighbour)
            if new_movement_cost_to_neighbour < neighbour.gcost or not open_positions.__contains__(neighbour):
                neighbour.gcost = new_movement_cost_to_neighbour
                neighbour.hcost = get_distance(neighbour, end_node)
                neighbour.parent = current_node

                if not open_positions.__contains__(neighbour):
                    open_positions.append(neighbour)
                    if neighbour != end_node:
                        neighbour.tile.set_state("open")


def reset():
    global start_node, end_node, nodes, path, open_positions, closed_positions
    start_node = None
    end_node = None
    nodes = []
    path = []
    open_positions = []
    closed_positions = []
    for tile in display.tiles:
        tile.reset_state()