import sys
import math


class player():
    def __init__ (self,x,y):
        self.x = x
        self.y = y

class cell():
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
    if cellB.x == cellA.x +1  and cellB.y == cellA.y :
        #going right
        for w in walls:
            if w.x == cellB.x and (w.y == cellB.y or w.y +1 == cellB.y):
                blocked = True
    if cellB.x == cellA.x -1  and cellB.y == cellA.y :
        #going left
        for w in walls:
            if w.x == cellB.x + 1 and (w.y == cellB.y or w.y +1 == cellB.y):
                blocked = True



# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]


players = []
walls = []
# game loop
while True:
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


    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
    if me.x==0:
        if blocked(me,cell(me.x+1,me.y)):
            print("UP")
        else:
            print("RIGHT")
    else:
        print("LEFT")
