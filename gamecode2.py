import sys
import math
import numpy
import time


## TODO make player a sub class of grid?
## 
## TODO see how many rounds we can play forwards
## add take turn code and valid turn code to allow move and wall type turns


## add specifc startegies for top bottom and middle starts

## only add a blocking wall if it makes the path longer
## or add the block that makes the oppo path longer by the most

## choose oppo who is nearest the finish

## code prediction tree v reactive

## woprk on luring oppo beyond limit of his search tree

# code best_block

## find all walls next to oppo, edge? or other walls or maybe within 1 of other things
## maybe find all 2 wall segments next to etc. and choose the one that adds the longest
## 3 wall segments?

class game():
    def __init__(self):
        self.turn = 0
        self.w = 9
        self.h = 9
        self.board = grid(w,h)
    
    def add_players(self,index,pos,player_data):
        self.board.add_player(index,pos,player_data)

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
        
    def __str__(self):
        return "["+str(self.dx)+","+str(self.dy)+"]"

    def __repr__(self):
        return "["+str(self.dx)+","+str(self.dy)+"]"
    
    def __eq__(self,other):
        return self.dx == other.dx and self.dy == other.dy
    

               
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
        return str("too big to print")
    
    def __repr__(self):
        return str("too big to print")
        
    def build_grid(self):
        self.cells = numpy.empty((w,h),"object")
        for i in range(w):
            for j in range(h):
                self.cells[i][j]=cell(i,j)
                
    def add_wall(self,new_wall):
        if new_wall not in self.walls:
            self.walls.append(new_wall)
        
    def remove_wall(self,old_wall):
        if old_wall in self.walls:
            self.walls.remove(old_wall)
    
    def add_player(self,index,pos,player_data):
        # create a player with reference back to this board
        self.players.append(player(index,pos,self,player_data))
        
    def move_player(self,i,m):
        self.players[i].move(m)
    
    def move_player_back(self,i,m):
        self.players[i].move_back(m)
    
    # how do we score a grid
    def grid_score(self,pl):
        a = -5
        b = 5
        c = 1
        d = -1
        e = -1
        pl_dist = len(pl.path_to_victory())
        oppos = (o for o in self.players if o != pl )
        oppo_dist = []
        oppo_walls = []
        for o in oppos:
            oppo_dist.append(len(o.path_to_victory()))
            oppo_walls.append(o.walls)
        
    
        score = 0
        # add a * the difference in length of path to victory for the best opponent
        score += a * pl_dist
        score += b * min(oppo_dist)
        score += c * pl.walls
        score += d * min(oppo_walls) 
        score += e * self.walls_ahead(pl)
        return score
    
    def walls_ahead(self,pl):
        wa = 0
        for w in self.walls:
            if pl.index == 0:
                if w.x>pl.position.x:
                    wa += 1
            if pl.index == 1:
                if w.x<pl.position.x:
                    wa += 1
            if pl.index == 2:
                if w.y>pl.position.y:
                    wa += 1
        return wa    
    
    def walls_behind(self,pl):
        w = 0
        for w in self.walls:
            if pl.index == 0:
                if w.x<pl.position.x:
                    wb += 1
            if pl.index == 1:
                if w.x>pl.position.x:
                    wb += 1
            if pl.index == 2:
                if w.y<pl.position.y:
                    wb += 1
        return wb    
       
    def won_by(self):
        winner = None
        for p in self.players:
            if p.won():
                winner = p
        return winner
                
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
        
        #does the move take you out of bounds        
        if position.x + move.dx > 8:
            valid = False
        if position.x + move.dx <0:
            valid = False
        if position.y + move.dy > 8:
            valid = False
        if position.y + move.dy <0:
            valid = False
           
        return valid
    
    # is it valid to place another wall with orintation on this grid
    def valid_wall(self,new_wall):
        print("wall check..."+ str(new_wall.y), file=sys.stderr, flush=True)
        valid = True
        if len(walls)>0:
            for w in walls:
                #idenical walls
                if w.o==new_wall.o and w.x==new_wall.x and w.y==new_wall.y:
                    valid = False
                #new wall 1 below an existing vertical wall
                elif w.o=="V" and new_wall.o == "V" and w.x==new_wall.x and w.y==new_wall.y+1:
                    valid = False
                #new wall 1 above an existing vertical wall
                elif w.o=="V" and new_wall.o == "V" and w.x==new_wall.x and w.y==new_wall.y-1:
                    valid = False       
                # new wall 1 to the left of a horizonal wall
                elif w.o=="H" and new_wall.o == "H" and w.x==new_wall.x-1 and w.y==new_wall.y:
                    valid = False
                # new wall 1 to the right of a horizonal wall
                elif w.o=="H" and new_wall.o == "H" and w.x==new_wall.x+1 and w.y==new_wall.y:
                    valid = False
                    
                #new vertical wall crossing a horizontal
                elif w.o=="H" and new_wall.o == "V" and w.x==new_wall.x-1 and w.y==new_wall.y+1:
                    valid = False
                #new Horizontal wall crossing a vertical
                elif w.o=="V" and new_wall.o == "H" and w.x==new_wall.x+1 and w.y==new_wall.y-1:
                    valid = False    
    
        # check even if no walls
        if new_wall.o == "H" and new_wall.x>=8:
            valid = False
        elif new_wall.o == "H" and new_wall.y<=0:
            valid = False
        elif new_wall.o == "H" and new_wall.x<0:
            valid = False
        elif new_wall.o == "V" and new_wall.y>=8:
            valid = False
        elif new_wall.o == "V" and new_wall.x<=0:
            valid = False
        elif new_wall.o == "V" and new_wall.y<0:
            valid = False
            
        # check for block-in
        self.add_wall(new_wall)
        print("checking for block in for "+str(new_wall), file=sys.stderr, flush=True)  
        for pl in self.players:
            if pl.position.x != -1 and not pl.path_to_victory():
                valid = False
        #return things to how they were
        self.remove_wall(new_wall)
    
        return valid
    
    def touching_walls(self):
        tw= []
        for w in self.walls:
            if w.o == "V":
                tw.append(wall(w.x-2,w.y,"H"))
                tw.append(wall(w.x-1,w.y,"H"))
                tw.append(wall(w.x,w.y,"H"))
                tw.append(wall(w.x-2,w.y+1,"H"))
                tw.append(wall(w.x,w.y+1,"H"))
                tw.append(wall(w.x-2,w.y+2,"H"))
                tw.append(wall(w.x-1,w.y+2,"H"))
                tw.append(wall(w.x,w.y+2,"H"))
                tw.append(wall(w.x,w.y-2,"V"))
                tw.append(wall(w.x,w.y+2,"V"))
            if w.o == "H":
                tw.append(wall(w.x-2,w.y,"H"))
                tw.append(wall(w.x,w.y,"V"))
                tw.append(wall(w.x+2,w.y,"H"))
                tw.append(wall(w.x,w.y-2,"V"))
                tw.append(wall(w.x+1,w.y-2,"V"))
                tw.append(wall(w.x+2,w.y-2,"V"))
                tw.append(wall(w.x+1,w.y,"V"))
                tw.append(wall(w.x+2,w.y,"V"))
                tw.append(wall(w.x,w.y-1,"V"))
                tw.append(wall(w.x+2,w.y-1,"V"))
          ## TODO deduplicate list      
        return tw
    
    def blocking_players(self):
        tp = []
        for pl in self.players:
            for i in range(self.w-1):
                tp.append(wall(i,pl.position.y,"V"))
                tp.append(wall(i,pl.position.y-1,"V"))
            for j in range(self.h-1):
                tp.append(wall(pl.position.x,j,"H"))
                tp.append(wall(pl.position.x-1,j,"H"))
        return tp
    
    def get_valid_neighbours(self,p):
        # return a list of positions that are reachable from position p 
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
    
    # shortest path between two cells on the grid
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
    def __init__ (self,index,position,board,walls = 0):
        self.index = index
        self.position = position
        self.walls = walls # number of wall elements left
        self.win = [] # list of positions that constitute winning the game
        self.board = board
    
    def __str__(self):
        return "["+str(self.index)+" @ "+str(self.position)+"]" 
    def __repr__(self):
        return "["+str(self.index)+" @ "+str(self.position)+"]"    
    
    def __eq__(self,other):
        return self.index == other.index and self.board==other.board
    
    # identify positions that count as a win if this player is on them
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
        for p in map.players:
            print("p.index self.index"+str(p.index)+","+str(self.index), file=sys.stderr, flush=True)  
        moves = route_to_moves(self.path_to_victory())
        return moves[0]  
    
    def move(self,m):
        self.position.x += m.dx
        self.position.y += m.dy
        
    def move_back(self,m):
        self.position.x -= m.dx
        self.position.y -= m.dy
    
    def won(self):
        
        if self.position in self.win:
            return True
        else:
            return False
    def all_turns(self):
        turns = []
        turns.append(move(0,-1))
        turns.append(move(0,1))
        turns.append(move(1,0))
        turns.append(move(-1,0))
        for i in range(9):
            for j in range(9):
                for k in ["V","H"]:
                    turns.append(wall(i,j,k))
        return turns

class wall():
    def __init__ (self,x,y,o):
        self.x=x
        self.y=y
        self.o=o
    
    def __str__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.o)+"]"

    def __repr__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.o)+"]"
      
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.o == other.o

    def to_text(self):
        return self.__str__()
        
        # game function not linked to a specific class
def all_turns():
    turns = []
    turns.append(move(0,-1))
    turns.append(move(0,1))
    turns.append(move(1,0))
    turns.append(move(-1,0))
    for i in range(9):
        for j in range(9):
            for k in ["V","H"]:
                turns.append(wall(i,j,k))
    return turns

# convert list of moves to text for the output
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
        current.x = i.x
        current.y = i.y
    return moves

def turn_to_text(t):
    if isinstance(t,move):
        if t.dx == 0 and t.dy == 1:
            return "DOWN"
        elif t.dx == 0 and t.dy == -1:
            return "UP"
        elif t.dx == 1:
            return "RIGHT"
        elif t.dx == -1:
            return "LEFT"
    elif isinstance(t,wall):
        return str(t.x)+" "+str(t.y)+" "+str(t.o)

def text_to_wall(t):
    return wall(t[0],t[2],t[3])

def text_to_turn(t):
    turn = None
    if t == "DOWN": turn = move(0,1)
    elif t == "UP": turn = move(0,-1)
    elif t == "LEFT": turn = move(-1,0)
    elif t == "RIGTH": turn = move(1,0)
    else: turn = text_to_wall (t)
    
    
    
def text_to_moves(text):
    return all_turns()[text]

# place a wall to block between to positions
def blocks(current,to):
    blocks=[]
    # if movement is up
    if current.x == to.x and current.y > to.y: 
        blocks.append(wall(current.x,current.y,"H"))
        blocks.append(wall(current.x-1,current.y,"H"))
     # if movement is down
    if current.x == to.x and current.y < to.y: 
        blocks.append(wall(to.x,to.y,"H"))
        blocks.append(wall(to.x-1,to.y,"H"))
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

# This is the minimax function. It considers all 
# the possible ways the game can go and returns 
# the value of the board 
def minimax(grid, depth, player) : 
    max_depth = 3
    score = grid.grid_score(player)
    isMax = False
    if player.index == my_id: isMax = True
    # If Maximizer has won the game return his/her 
    # evaluated score 
    if (score == 1000) : 
        return score
  
    # If Minimizer has won the game return his/her 
    # evaluated score 
    if (score == -1000) :
        return score
    
    if depth == max_depth:
        return score
  
    # If this maximizer's move 
    if (isMax) :     
        best = -10000
  
        # Traverse all move options 
        for t in all_turns():
               
                # Check if t is valid
                if is_valid_turn(t) :
                  
                    # Make the move 
                    grid.take_turn(t,player)
                    # Call minimax recursively and choose 
                    # the maximum value 
                    best = max( best, minimax(grid, depth + 1,grid.players[player.index+1 % player_count]))
  
                    # Undo the move 
                    grid.undo_turn(t,player)
        return best
  
    # If this minimizer's move 
    else :
        best = 10000
  
        # Traverse all move options 
        for t in all_turns():
               
                # Check if t is valid
                if is_valid_turn(t) :
                  
                    # Make the move 
                    grid.take_turn(t,player)
                    # Call minimax recursively and choose 
                    # the maximum value 
                    best = min( best, minimax(grid, depth + 1,grid.players[player.index+1 % player_count]))
  
                    # Undo the move 
                    grid.undo_turn(t,player)
        return best
  
# This will return the best possible move for the player 
def findBestMove(grid) : 
    bestVal = -1000 
    bestMove = -1 
  
    # Traverse all cells, evaluate minimax function for 
    # all empty cells. And return the cell with optimal 
    # value. 
    for t in all_turns():
          
            # Check if t is valid
            if is_valid_turn(t) :
              
                # Make the move 
                grid.take_turn(t,player)
                # compute evaluation function for this 
                # move. 
                moveVal = minimax(grid, 0, False) 
  
                # Undo the move 
                grid.undo_turn(t,player)
  
                # If the value of the current move is 
                # more than the best value, then update 
                # best/ 
                if (moveVal > bestVal) :                
                    bestMove = t
                    bestVal = moveVal
  
    print("The value of the best Move is :", bestVal)
    print()
    return bestMove

def is_valid_turn(t ,p: player):
    if isinstance(t,str):
        t= text_to_turn(t)
    valid = False
    if isinstance(t,wall):
        valid = map.valid_wall(t)
    if isinstance(t,move):
        valid = map.valid_move(p.position,t)
    return valid

def best_turns():
    turns = []
    turns.append(move(0,-1))
    turns.append(move(0,1))
    turns.append(move(1,0))
    turns.append(move(-1,0))
    turns.extend(map.touching_walls())
    turns.extend(map.blocking_players())
    print("best Turns = "+ str(turns), file=sys.stderr, flush=True)
    
    return turns

def best_move(player):
    current_score = map.grid_score(me)
    best_score = -10000
    best_move = None

    for t in best_turns():
        print("checking = "+ str(t), file=sys.stderr, flush=True)
        if is_valid_turn(t,player):
            print("Valid = "+ str(t), file=sys.stderr, flush=True)
            if isinstance(t,wall):
                map.add_wall(t)
                new_score = map.grid_score(me)
                if new_score > best_score:
                    best_score = new_score
                    best_move = t
                map.remove_wall(t)
            if isinstance(t,move):
                map.move_player(player.index,t)
                new_score = map.grid_score(me)
                if new_score > best_score:
                    best_score = new_score
                    best_move = t
                map.move_player_back(player.index,t)
    return best_move       
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]


    
game_turn = 0

## replace text with move and wall objects
strategy = ""
strategy_89 = ["1 7 H","3 7 H","LEFT","5 7 H","LEFT","7 7 V"]
strategy_12 = ["1 2 H","3 2 H","LEFT","5 2 H","LEFT","7 0 V"]

strategy_89L = ["6 7 H","4 7 H","RIGHT","2 7 H","RIGHT","1 7 V","RIGHT","0 7 H"]  
strategy_12L = ["6 2 H","4 2 H","RIGHT","2 2 H","RIGHT","1 0 V","RIGHT","0 2 H"]

strategy_45 = ["LEFT","8 6 V","8 2 V","6 8 H","4 8 H","2 8 H","8 4 V","LEFT","LEFT","8 0 V"]
strategy_45L = ["RIGHT","1 6 V","1 2 V","1 8 H","3 8 H","5 8 H","1 4 V","RIGHT","RIGHT","1 0 V"]
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
        map.add_player(i,position(x,y),walls_left)
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        inputs = input().split()
        wall_x = int(inputs[0])  # x-coordinate of the wall
        wall_y = int(inputs[1])  # y-coordinate of the wall
        wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
        walls.append(wall(wall_x,wall_y,wall_orientation))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # print("map.players = "+ str(map.players), file=sys.stderr, flush=True)
    
    # choose oppo
    if my_id == 2: oppo_id = 1
    if my_id == 0: oppo_id = 1
    if my_id ==1: oppo_id = 0
    
    for i in range(h):
        map.players[0].add_winning_position(position(8,i))
        map.players[1].add_winning_position(position(0,i))
    if player_count ==3:
        for i in range(w):
            map.players[2].add_winning_position(position(i,8))
    
    for new_wall in walls:
        map.add_wall(new_wall)
        
    me = map.players[my_id]
    my_dist = len(me.path_to_victory())

    oppo = map.players[oppo_id]
    oppo_dist = len(oppo.path_to_victory())
       

    
   # setup for each turn
    if game_turn <3:
        if oppo.position in [position(1,7),position(1,8)]:strategy = "89"
        if oppo.position in [position(1,1),position(1,0)]:strategy = "12"
        if oppo.position in [position(8,1),position(8,0)]:strategy = "12L" 
        if oppo.position in [position(8,7),position(8,8)]:strategy = "89L"
        if oppo.position in [position(8,4),position(8,5)]:strategy = "45L" 
        if oppo.position in [position(1,4),position(0,4),position(1,5),position(0,5)]:strategy = "45"  
           
    if strategy == "89":
        if strategy_89:
            output = strategy_89.pop(0)
        else:
            strategy = ""
    
    if strategy == "12":
        if strategy_12:
            output = strategy_12.pop(0)
        else:
            strategy = ""
    if strategy == "89L":
        if strategy_89L:
            output = strategy_89L.pop(0)
        else:
            strategy = ""
    if strategy == "12L":
        if strategy_12L:
            if is_valid_turn(strategy_12L[0],me):
                output = strategy_12L.pop(0)
        else:
            strategy = ""
            
    if strategy == "45":
        if strategy_45:
            output = strategy_45.pop(0)
        else:
            strategy = ""
    
    if strategy == "45L":
        if strategy_45L:
            output = strategy_45L.pop(0)
        else:
            strategy = ""
    
    if strategy == "" or output=="":
        print("strategy = "+ str(strategy), file=sys.stderr, flush=True)
        print("Grid score = "+ str(map.grid_score(me)), file=sys.stderr, flush=True)
        # if me dist >= oppo dist - test block
        print("my dist..."+ str(my_dist), file=sys.stderr, flush=True)
        print(me.path_to_victory(), file=sys.stderr, flush=True)
        print("oppo dist..."+ str(oppo_dist), file=sys.stderr, flush=True)
        print(oppo.path_to_victory(), file=sys.stderr, flush=True)
        #block = blocks(oppo.position,oppo.path_to_victory()[1])
        #if my_dist > oppo_dist and block and me.walls != 0:
        #    output = str(block[0].x)+" "+str(block[0].y)+" "+str(block[0].o)
        #else:
        #    output = me.next_move() 
        
        output = turn_to_text(best_move(me))
        
        ## TODO allow for if you are player 0,1,2 to account for if this should be > or >=
        
        end = time.process_time()-start
        print("time for this round"+ str(end), file=sys.stderr, flush=True)
        
        
    print(output)




