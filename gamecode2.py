import sys
import math
import numpy
import time


class game():
    pass

class position():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "P"+str(self.x)+","+str(self.y)+"P"

    def __repr__(self):
        return "PP"+str(self.x)+","+str(self.y)+"PP"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
class move():
    def __init__(self,dx,dy):
        self.dx = dx
        self.dy = dy

class cell():
    def __init__ (self,position,data = None):
        self.position = position
        self.data = data
        
    def __str__(self):
        return str(self.position)+":"+str(self.data)

class grid():
    def __init__(self,w : int,h : int,cells : list[cell] = []):
        self.w = w
        self.h = h
        self.cells = cells
        self.walls = []
        self.players = []
        
        self.build_grid()
        
        
    def __str__(self):
        return str(self.cells[7][1])
        
    def build_grid(self):
        self.cells = numpy.empty((w,h),"object")
        for i in range(w):
            for j in range(h):
                self.cells[i][j]=cell(i,j)
                
    def add_walls(self,walls):
        self.walls = walls
    
    def add_player(self,id,x,y,player_data):
        # create a player with reference back to this board
        self.players.append(player(id,position(x,y),self,player_data))
                
    def astar(self,start):
        pass

    def valid_wall(self,x,y):
        pass
    
    # for a given position is a move valid
    def valid_move(self,position,move):
        valid = True
        # is the moved blocked by a wall
        for w in self.walls:
            if w.o == "V" and move.dx ==1 and w.x == position.x+1 and (w.y == position.y or w.y+1 == position.y):
                valid = False
                print("blocked right", file=sys.stderr, flush=True)
            elif w.o == "V" and move.dx == -1 and w.x == position.x and (w.y == position.y or w.y+1 == position.y):
                valid = False
                print("blocked left", file=sys.stderr, flush=True)
            elif w.o == "H" and move.dy == 1 and w.y == position.y+1 and (w.x == position.x or w.x+1 == position.x):
                valid = False
                print("blocked Down", file=sys.stderr, flush=True)
            elif w.o == "H" and move.dy == -1 and w.y == position.y and (w.x == position.x or w.x+1 == position.x):
                valid = False
                print("blocked up", file=sys.stderr, flush=True)
        if position.x + move.dx > 8:
            valid = False
            print("Right edge", file=sys.stderr, flush=True)
        if position.x + move.dx <0:
            valid = False
            print("left edge", file=sys.stderr, flush=True)
        if position.y + move.dy > 8:
            valid = False
            print("bottom edge", file=sys.stderr, flush=True)
        if position.y + move.dy <0:
            valid = False
            print("top edge", file=sys.stderr, flush=True)
        return valid
    
    def get_valid_neighbours(self,p):
        # return a list of positions that are the neighbours of p 'position'
        neighbours = []
        # is up valid
        if self.valid_move(p,move(0,-1)):
            neighbours.append(position(p.x,p.y-1))
        #is down valid
        if self.valid_move(p,move(0,1)):    
            neighbours.append(position(p.x,p.y+1))
        # is left valid
        if self.valid_move(p,move(-1,0)):
            neighbours.append(position(p.x-1,p.y))
        # is right valid
        if self.valid_move(p,move(1,0)):
            neighbours.append(position(p.x+1,p.y))

        return neighbours
    
    def shortest_path(self, node1, node2):
        path_list = [[node1]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = [node1]
        if node1 == node2:
            return path_list[0]
            
        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
                
            next_nodes = self.get_valid_neighbours(last_node)
            
            # Search goal node
            if node2 in next_nodes:
                current_path.append(node2)
                return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes:
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    # To avoid backtracking
                    previous_nodes.append(next_node)
            # Continue to next path in list
            path_index += 1
        # No path is found
        return []   

    

class player():
    def __init__ (self,id,position,board,walls = 0,win = []):
        self.id =id
        self.position = position
        self.walls = walls # number of wall elements left
        self.win = [] # list of positions that constitute winning the game
        self.board = board
        
    def length_to_win(self):
        pass
    
    def add_winning_position(self,position):
        self.win.append(position)
        
    def path_to_victory(self):
        path_list = [[self.position]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = [self.position]
        if self.position in self.win:
            return path_list[0]
            
        while path_index < len(path_list):
            
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = self.board.get_valid_neighbours(last_node)
            print("last node - "+str(last_node), file=sys.stderr, flush=True)
            print("next nodes - "+str(next_nodes), file=sys.stderr, flush=True)
            # Search goal node
            for w in self.win:  
                if w in next_nodes:
                    current_path.append(w)
                    return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes:
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    # To avoid backtracking
                    previous_nodes.append(next_node)
            # Continue to next path in list
            if path_index % 10 == 0:
                ## add time stamp 
                end = time.process_time()
                duration = end - start
                print(output + " :"+str.format('{0:.8f}', duration), file=sys.stderr, flush=True)
                ## 
            path_index += 1
        # No path is found
        return []   
       
class wall():
    def __init__ (self,x,y,o):
        self.x=x
        self.y=y
        self.o=o


def all_turns():
    turns = []
    turns.append("UP")
    turns.append("DOWN")
    turns.append("RIGHT")
    turns.append("LEFT")
    for i in range(8):
        for j in range(8):
            for k in ["V","H"]:
                turns.append([i,j,k])
    return turns


# given a set of walls, is it valid to place another wall with orintation o in position x,y
def valid_wall(walls,x,y,o):
    valid = True
    for w in walls:
        if w.o==o and w.x==x and w.y==y:
            valid = False
        elif w.o=="V" and o == "V" and w.x==x and w.y==y+1:
            valid = False
        elif w.o=="H" and o == "H" and w.x==x-1 and w.y==y:
            valid = False
        elif w.o != o and w.x==x-1 and w.y==y+1:
            valid = False
        elif o == "H" and x>=8:
            valid = False
        elif o == "V" and y>=8:
            valid = False
    return valid

def route_to_moves(route):
    current = route.pop(0)
    moves = []
    for i in route:
        dx = i.x - current.x
        dy = i.y - current.y
        if dx == 0 and dy==1:
            moves.append("DOWN")
        elif dx == 0 and dy == -1:
            moves.append("UP")
        elif dx     == 1 and dy == 0:
            moves.append("RIGHT")
        elif dx == -1 and dy == 0:
            moves.append("LEFT")
        else:
            moves.append("????")
    return moves

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]


game_turn = 0
end = ""
# game loop
while True:
    # measure the time at the start of a loop
    start = time.process_time()
    
    
    game_turn += 1
    players = []
    walls = []
    output = ""
    
    map = grid(w,h)
    
    # get turn data from standard input stream
    for i in range(player_count):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # walls_left: number of walls available for the player
        x, y, walls_left = [int(j) for j in input().split()]
        map.add_player(id,x,y,walls_left)
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        inputs = input().split()
        wall_x = int(inputs[0])  # x-coordinate of the wall
        wall_y = int(inputs[1])  # y-coordinate of the wall
        wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
        walls.append(wall(wall_x,wall_y,wall_orientation))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    me = map.players[my_id]

    if my_id==0:
        end = "RIGHT"
        for i in range(h):
            map.players[my_id].add_winning_position(position(8,i))
    elif my_id==1:
        end = "LEFT"
        for i in range(h):
            map.players[my_id].add_winning_position(position(0,i))
    else:
        end = "BOTTOM"
        for i in range(w):
            map.players[my_id].add_winning_position(position(i,8))
        
    
    
    
    
    
    # setup for each turn
    map.add_walls(walls)
    
    print("me "+str(me.position), file=sys.stderr, flush=True)
    
    next_nodes = me.board.get_valid_neighbours(position(8,2))
    print("me valid neighbours"+str(next_nodes), file=sys.stderr, flush=True)
    # turns = all_turns()
    route = map.players[my_id].path_to_victory()
    print("route  "+str(route), file=sys.stderr, flush=True)
    moves = route_to_moves(route)
    
    output = moves[0] 
    # meansure the time just beofre printing
    end = time.process_time()
    duration = end - start
    print(output + " :"+str.format('{0:.8f}', duration))
