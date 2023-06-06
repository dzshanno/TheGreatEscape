import sys
import math
import numpy
import time

class position():
    def __initi__(self,x,y):
        self.x = x
        self.y = y
        
    def __str___(self):
        return "["+str(self.x)+","+str(self.y)+"]"

class cell():
    def __init__ (self,position,data = None):
        self.position = position
        self.data = data
        
    def __str__(self):
        return str(self.position)+":"+str(self.data)
    
    
        
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
        self.walls = []
        self.players = []
        
    def __str__(self):
        return str(self.cells[7][1])
        
    def build_grid(self):
        self.cells = numpy.empty((w,h),"object")
        for i in range(w):
            for j in range(h):
                self.cells[i][j]=cell(i,j)
                
    def add_walls(self,walls):
        self.walls = walls
    
    def add_player(self,x,y,player_data):
        # create a player with reference back to this board
        self.players.append(player(x,y,self,walls))
                
    def astar(self,start):
        pass

    def valid_wall(self,x,y):
        pass
    
    # for a given player is a move valid
    def valid_move(self,player,move):
        valid = True
        # is the moved blocked by a wall
        for w in self.walls:
            if w.o == "V" and move.x ==1 and w.x == player.x+1 and (w.y == player.y or w.y+1 == player.y):
                valid = False
            elif w.o == "V" and move.x == -1 and w.x == player.x and (w.y == player.y or w.y+1 == player.y):
                valid = False
            elif w.o == "H" and move.y == 1 and w.y == player.y-1 and (w.x == player.x or w.x+1 == player.x):
                valid = False
            elif w.o == "H" and move.y == -1 and w.y == player.y and (w.x == player.x or w.x+1 == player.x):
                valid = False
        if player.x + move.x > 8:
            valid = False
        if player.x + move.x <0:
            valid = False
        if player.y + move.y > 8:
            valid = False
        if player.y + move.y <0:
            valid = False
        #if no paths are available for any player
        for p in self.players:
            if p.length_to_win()==--1:
                valid = False
        return valid
    
        



class player():
    def __init__ (self,x,y,board,walls = 0,win = []):
        self.x = x
        self.y = y
        self.walls = walls # number of wall elements left
        self.win = [] # cells that constitute winning the game
        self.board = board
        
    def length_to_win():
        pass
       
class wall():
    def __init__ (self,x,y,o):
        self.x=x
        self.y=y
        self.o=o


def all_turns():
    turns = []
    turns.extend([[0,-1],[0,1],[-1,0],[1,0]])
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
    
    
    # setup for each turn
    map.add_walls(walls)
   
    output = "RIGHT" 
    # meansure the time just beofre printing
    end = time.process_time()
    duration = end - start
    print(output + " :"+str.format('{0:.8f}', duration))
