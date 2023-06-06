import sys
import math
import numpy




class cell():
    def __init__ (self,x,y,links = []):
        self.x = x
        self.y = y
        self.links = links
        self.win = False
        self.score = 0
        
    def __str__(self):
        return "["+str(self.x)+","+str(self.y)+"]-["+str(self.links)+"]"
    
        
class Node():
    # A node class for A* Pathfinding

    def __init__(self, x,y,parent = None):
        self.parent = parent
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.index == other.index

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index)

class grid():
    def __init__(self,w : int,h : int,cells : list[cell] = []):
        self.w = w
        self.h = h
        self.cells = cells
        
    def __str__(self):
        return str(self.cells[7][1])
        
    def build_grid(self):
        self.cells = numpy.empty((w,h),"object")
        for i in range(w):
            for j in range(h):
                neighbours = []
                if i>0:
                    neighbours.append([i-1,j])
                if i<(w-1):
                    neighbours.append([i+1,j])
                if j>0:
                    neighbours.append([i,j-1])
                if j<(h-1):
                    neighbours.append([i,j+1])
                self.cells[i][j]=cell(i,j,neighbours)
                
    def add_walls(self,walls):
        for w in walls:
            if w.o == "V":
                if [w.x,w.y] in self.cells[w.x-1][w.y].links:
                    self.cells[w.x-1][w.y].links.remove([w.x,w.y])
                if [w.x-1,w.y] in self.cells[w.x][w.y].links:
                    self.cells[w.x][w.y].links.remove([w.x-1,w.y])
                if [w.x,w.y+1] in self.cells[w.x-1][w.y+1].links:
                    self.cells[w.x-1][w.y+1].links.remove([w.x,w.y+1])
                if [w.x-1,w.y+1] in self.cells[w.x][w.y+1].links:
                    self.cells[w.x][w.y+1].links.remove([w.x-1,w.y+1])
         
    def set_win(self,direction):
        if direction == "RIGHT":
            for j in range(h):
                self.cells[w-1][j].win = True
        if direction == "LEFT":
            for j in range(h):
                self.cells[0][j].win = True
                
    def astar(self,start):
        pass

    def valid_wall(self,x,y):
        pass



class player():
    def __init__ (self,x,y):
        self.x = x
        self.y = y
       
class wall():
    def __init__ (self,x,y,o):
        self.x=x
        self.y=y
        self.o=o
# is the route from cellA to cellB blocked
def blocked(cellA,cellB):
    blocked = False
    print("A "+str([cellA.x,cellA.y])+" B: "+str([cellB.x,cellB.y]), file=sys.stderr, flush=True)
    if cellB.x == cellA.x +1  and cellB.y == cellA.y :
        #going right
        print("going right", file=sys.stderr, flush=True)
        for w in walls:
            
            print("wall "+str([w.x,w.y]), file=sys.stderr, flush=True)
            if w.x == cellB.x and (w.y == cellB.y or w.y +1 == cellB.y):
                blocked = True
    if cellB.x == cellA.x -1  and cellB.y == cellA.y :
        #going left
        print("going left", file=sys.stderr, flush=True)
        for w in walls:
            
            print("wall "+str([w.x,w.y]), file=sys.stderr, flush=True)
            if w.x == cellB.x + 1 and (w.y == cellB.y or w.y +1 == cellB.y):
                blocked = True
    return blocked


def valid_wall(walls,x,y,o):
    valid = True
    for w in walls:
        if w.o=="V" and o == "V" and w.x==x and w.y==y:
            valid = False
        elif w.o=="V" and o == "V" and w.x==x and w.y==y+1:
            valid = False
        elif w.o=="H" and o == "H" and w.x==x and w.y==y:
            valid = False
        elif w.o=="H" and o == "H" and w.x==x-1 and w.y==y:
            valid = False
    return valid

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
    game_turn += 1
    players = []
    walls = []
    output = ""
    
    for i in range(player_count):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # walls_left: number of walls available for the player
        x, y, walls_left = [int(j) for j in input().split()]
        players.append(player(x,y))
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        inputs = input().split()
        wall_x = int(inputs[0])  # x-coordinate of the wall
        wall_y = int(inputs[1])  # y-coordinate of the wall
        wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
        walls.append(wall(wall_x,wall_y,wall_orientation))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    me = cell(players[my_id].x,players[my_id].y)

    if my_id==0:
        end = "RIGHT"
    elif my_id==1:
        end = "LEFT"
    else:
        end = "BOTTOM"
       
    map = grid(w,h)
    map.build_grid()
    map.set_win(end)
    
    
    # setup for each turn
    map.add_walls(walls)
    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall  
    
    ## check to see if opponent is about to win and block them
    for i in range(player_count):
        if i == my_id:
            pass
        elif i == 0:
            if players[i].x==6:
                if valid_wall(walls,7,min([players[i].y,7]),"V"):
                    output="7 "+str(min([players[i].y,7]))+" V"
                else:
                    output="8 "+str(min([players[i].y,7]))+" V"
        elif i == 1:
            if players[i].x==2:
                output = "1 "+str(min([players[i].y,7]))+" V"
        elif i ==2:
            if players[i].y==6:
                output = str(min([players[i].x,7]))+" 7 H"      
    
    if not output:
            if my_id==0:
                if [me.x+1,me.y] in map.cells[me.x][me.y].links:
                    output = "RIGHT"
                else:
                    output = "UP"
            if my_id==1:
                if [me.x-1,me.y] in map.cells[me.x][me.y].links:
                    output = "LEFT"
                else:
                    output = "UP"
            if my_id==2:
                if [me.x,me.y+1] in map.cells[me.x][me.y].links:
                    output = "DOWN"
                else:
                    output = "LEFT" 
    print(output)
