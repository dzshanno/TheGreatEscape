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
        return "["+str(self.x)+","+str(self.y)+"]"

    def __repr__(self):
        return "["+str(self.x)+","+str(self.y)+"]"

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
        
    def remove_walls(self,walls):
        for w in walls:
            if w in self.walls:
                self.walls.remove(w)
    
    def add_player(self,id,x,y,player_data):
        # create a player with reference back to this board
        self.players.append(player(id,position(x,y),self,player_data))
                
    def astar(self,start):
        pass

    
    # for a given position is a move valid
    def valid_move(self,position,move):
        valid = True
        # is the moved blocked by a wall
        for w in self.walls:
            if w.o == "V" and move.dx ==1 and w.x == position.x+1 and (w.y == position.y or w.y+1 == position.y):
                valid = False
                
            elif w.o == "V" and move.dx == -1 and w.x == position.x and (w.y == position.y or w.y+1 == position.y):
                valid = False
              
            elif w.o == "H" and move.dy == 1 and w.y == position.y+1 and (w.x == position.x or w.x+1 == position.x):
                valid = False
                
            elif w.o == "H" and move.dy == -1 and w.y == position.y and (w.x == position.x or w.x+1 == position.x):
                valid = False
             
        if position.x + move.dx > 8:
            valid = False
            
        if position.x + move.dx <0:
            valid = False
           
        if position.y + move.dy > 8:
            valid = False
            
        if position.y + move.dy <0:
            valid = False
           
        return valid
    
    # given a set of walls, is it valid to place another wall with orintation o in position x,y
    def valid_wall(self,p):
        print("wall check..."+ str(p.y), file=sys.stderr, flush=True)
        valid = True
        for w in walls:
            #idenical walls
            if w.o==p.o and w.x==p.x and w.y==p.y:
                valid = False
            #new wall 1 below an existing vertical wall
            elif w.o=="V" and p.o == "V" and w.x==p.x and w.y==p.y+1:
                valid = False
            #new wall 1 above an existing vertical wall
            elif w.o=="V" and p.o == "V" and w.x==p.x and w.y==p.y-1:
                valid = False       
            # new wall 1 to the left of a horizonal wall
            elif w.o=="H" and p.o == "H" and w.x==p.x-1 and w.y==p.y:
                valid = False
            # new wall 1 to the right of a horizonal wall
            elif w.o=="H" and p.o == "H" and w.x==p.x+1 and w.y==p.y:
                valid = False
                
            #new vertical wall crossing a horizontal
            elif w.o=="H" and p.o == "V" and w.x==p.x-1 and w.y==p.y+1:
                valid = False
            #new Horizontal wall crossing a vertical
            elif w.o=="V" and p.o == "H" and w.x==p.x+1 and w.y==p.y-1:
                valid = False    

        # check even if no walls
        if p.o == "H" and p.x>=8:
            valid = False
        elif p.o == "V" and p.y>=8:
            valid = False
        elif p.o == "H" and p.y<=0:
            valid = False
        elif p.o == "V" and p.x<=0:
            valid = False
            
            
        # TODO need to add check for 'still a valid path'
        map.add_walls(p)
        for p in map.players:
            if not p.path_to_victory():
                valid = False
        map.remove_walls(p)
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
    def __init__ (self,index,position,board,walls = 0,win = []):
        self.index = index
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
            path_index += 1
        # No path is found
        return []
    
    def next_move(self):
        moves = route_to_moves(self.path_to_victory())
        return moves[0]  
       
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

def blocks(current,to):
    blocks=[]
    # if movement is up
    if current.x == to.x and current.y > to.y: 
        blocks.append(wall(current.x,current.y,"H"))
        blocks.append(wall(current.x+1,current.y,"H"))
     # if movement is down
    if current.x == to.x and current.y < to.y: 
        blocks.append(wall(to.x,to.y,"H"))
        blocks.append(wall(to.x+1,to.y,"H"))
    # if movement is right
    if current.y == to.y and current.x < to.x:
        blocks.append(wall(to.x,to.y,"V"))
        blocks.append(wall(to.x,to.y-1,"V"))
    # if movement is left
    if current.y == to.y and current.x > to.x:
        blocks.append(wall(current.x,current.y,"V"))
        blocks.append(wall(current.x,current.y-1,"V"))
    
    if not map.valid_wall(blocks[1]): blocks.pop(1)
    if not map.valid_wall(blocks[0]): blocks.pop(0)
            
    return blocks

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]


    
game_turn = 0
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
        map.add_player(i,x,y,walls_left)
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        inputs = input().split()
        wall_x = int(inputs[0])  # x-coordinate of the wall
        wall_y = int(inputs[1])  # y-coordinate of the wall
        wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
        walls.append(wall(wall_x,wall_y,wall_orientation))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    for p in map.players:
        if p.position.x != -1 and p.index != my_id:
            oppo_id = p.index

    for i in range(h):
        map.players[0].add_winning_position(position(8,i))
    for i in range(h):
        map.players[1].add_winning_position(position(0,i))
    if player_count ==3:
        for i in range(w):
            map.players[2].add_winning_position(position(i,8))
    
    map.add_walls(walls)
        
    me = map.players[my_id]
    my_dist = len(me.path_to_victory())

    oppo = map.players[oppo_id]
    oppo_dist = len(oppo.path_to_victory())
       

    
   # setup for each turn
    
    
    # if me dist >= oppo dist - test block
    print("my dist..."+ str(my_dist), file=sys.stderr, flush=True)
    print("oppo dist..."+ str(oppo_dist), file=sys.stderr, flush=True)
    print(oppo.path_to_victory(), file=sys.stderr, flush=True)
    block = blocks(oppo.position,oppo.path_to_victory()[1])
    if my_dist >= oppo_dist and block and me.walls != 0:
        output = str(block[0].x)+" "+str(block[0].y)+" "+str(block[0].o)
    else:
        output = me.next_move() 
    
    print(output)


