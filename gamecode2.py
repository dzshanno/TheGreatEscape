import sys
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


def set_bit(value, bit):
    return value | (1 << bit)


def reset_bit(value, bit):
    return value & (~(1 << bit))


def check_bit(value, bit):
    return (value >> bit) & 1


class state:
    def __init__(self):
        self.con = [0, 0, 0, 0]  # 4 81 bit integers up/right/down/left
        self.pl_pos = [0, 0, 0]
        self.pl_wall = [0, 0, 0]
        self.walls = []
        self.players = []
        self.wallcentres = 0

    def is_valid_turn(self, pl, t):
        if isinstance(t, str):
            t = text_to_turn(t)
        valid = False
        if isinstance(t, wall):
            valid = g.valid_wall(t)
        if isinstance(t, move):
            valid = g.valid_move(pl.position, t)
        return valid

    def take_turn(self, pl, t):
        if isinstance(t, str):
            t = text_to_turn(t)
        if isinstance(t, wall):
            # print("setting wall:" + str(t), file=sys.stderr, flush=True)
            self.set_wall(t)
        elif isinstance(t, move):
            self.move_player(pl, t)
        else:
            print(
                "did not understand move:" + str(type(t)), file=sys.stderr, flush=True
            )

    def undo_turn(self, pl, t):
        if isinstance(t, str):
            t = text_to_turn(t)
        if isinstance(t, wall):
            self.reset_wall(t)
        if isinstance(t, move):
            self.unmove_player(pl, t)

    def set_wall(self, wall):
        pos = wall.x + (wall.y * w)
        type = wall.o
        if type == "H":
            self.con[0] = reset_bit(self.con[0], pos)
            self.con[0] = reset_bit(self.con[0], pos + 1)
            self.con[2] = reset_bit(self.con[2], pos - w)
            self.con[2] = reset_bit(self.con[2], pos - w + 1)
            self.wallcentres = set_bit(self.wallcentres, pos + 1)
        else:
            self.con[1] = reset_bit(self.con[1], pos - 1)
            self.con[1] = reset_bit(self.con[1], pos + w - 1)
            self.con[3] = reset_bit(self.con[3], pos)
            self.con[3] = reset_bit(self.con[3], pos + w)
            self.wallcentres = set_bit(self.wallcentres, pos + w)
        self.walls.append(wall)
        print(
            "wall entres = " + str(bin(self.wallcentres)), file=sys.stderr, flush=True
        )

    def reset_wall(self, wall):
        pos = wall.x + (wall.y * w)
        type = wall.o
        if type == "H":
            self.con[0] = set_bit(self.con[0], pos)
            self.con[0] = set_bit(self.con[0], pos + 1)
            self.con[2] = set_bit(self.con[2], pos - w)
            self.con[2] = set_bit(self.con[2], pos - w + 1)
        else:
            self.con[1] = set_bit(self.con[1], pos - 1)
            self.con[1] = set_bit(self.con[1], pos + w - 1)
            self.con[3] = set_bit(self.con[3], pos)
            self.con[3] = set_bit(self.con[3], pos + w)
        self.walls.remove(wall)

    def move_player(self, player, move):
        self.pl_pos[player.index] += move.dx + (move.dy) * w
        self.players[player.index].position.x += move.dx
        self.players[player.index].position.y += move.dy

    def unmove_player(self, player, move):
        self.pl_pos[player.index] -= move.dx + (move.dy) * w
        self.players[player.index].position.x -= move.dx
        self.players[player.index].position.y -= move.dy

    def touching_walls(self):
        tw = []
        for w in self.walls:
            if w.o == "V":
                tw.append(wall(w.x - 2, w.y, "H"))
                tw.append(wall(w.x - 1, w.y, "H"))
                tw.append(wall(w.x, w.y, "H"))
                tw.append(wall(w.x - 2, w.y + 1, "H"))
                tw.append(wall(w.x, w.y + 1, "H"))
                tw.append(wall(w.x - 2, w.y + 2, "H"))
                tw.append(wall(w.x - 1, w.y + 2, "H"))
                tw.append(wall(w.x, w.y + 2, "H"))
                tw.append(wall(w.x, w.y - 2, "V"))
                tw.append(wall(w.x, w.y + 2, "V"))
            if w.o == "H":
                tw.append(wall(w.x - 2, w.y, "H"))
                tw.append(wall(w.x, w.y, "V"))
                tw.append(wall(w.x + 2, w.y, "H"))
                tw.append(wall(w.x, w.y - 2, "V"))
                tw.append(wall(w.x + 1, w.y - 2, "V"))
                tw.append(wall(w.x + 2, w.y - 2, "V"))
                tw.append(wall(w.x + 1, w.y, "V"))
                tw.append(wall(w.x + 2, w.y, "V"))
                tw.append(wall(w.x, w.y - 1, "V"))
                tw.append(wall(w.x + 2, w.y - 1, "V"))
        return tw

    def blocking_players(self):
        tp = []
        for pl in self.players:
            if pl != me:
                for i in range(self.w - 1):
                    tp.append(wall(i, pl.position.y, "V"))
                    tp.append(wall(i, pl.position.y - 1, "V"))
                for j in range(self.h - 1):
                    tp.append(wall(pl.position.x, j, "H"))
                    tp.append(wall(pl.position.x - 1, j, "H"))
        return tp

    def touching_players(self):
        tp = []
        for pl in self.players:
            tp.append(wall(pl.position.x, pl.position.y, "V"))
            tp.append(wall(pl.position.x + 1, pl.position.y, "V"))
            tp.append(wall(pl.position.x, pl.position.y - 1, "V"))
            tp.append(wall(pl.position.x + 1, pl.position.y - 1, "V"))
            tp.append(wall(pl.position.x, pl.position.y, "H"))
            tp.append(wall(pl.position.x - 1, pl.position.y, "H"))
            tp.append(wall(pl.position.x, pl.position.y + 1, "H"))
            tp.append(wall(pl.position.x - 1, pl.position.y + 1, "H"))
        return tp


class game:
    def __init__(self):
        self.turn = 0
        self.w = 9
        self.h = 9
        self.board = grid(w, h)
        self.state = state()
        self.pl_won = [0, 0, 0]
        self.depth = 0

        # setup all connections
        for i in range(4):
            self.state.con[i] = (1 << 81) - 1

        # remove edges

        for i in range(w):
            self.state.con[0] = reset_bit(self.state.con[0], i)
            self.state.con[1] = reset_bit(self.state.con[1], i * 9 + 8)
            self.state.con[2] = reset_bit(self.state.con[2], i + 9 * (8))
            self.state.con[3] = reset_bit(self.state.con[3], i * 9)
        # prepare win-condition masks
        for i in range(w):
            self.pl_won[0] = set_bit(self.pl_won[0], (i * 9 + 8))
            self.pl_won[1] = set_bit(self.pl_won[1], i * 9)
            self.pl_won[2] = set_bit(self.pl_won[2], (8) * 9 + i)

    def add_player(self, pl):
        self.state.pl_pos[pl.index] = pl.position.x + pl.position.y * w
        self.state.pl_wall[pl.index] = pl.walls
        self.state.players.append(pl)

    def valid_move(self, position, move):
        pos = position.x + (9 * position.y)
        if move.dy == -1 and check_bit(self.state.con[0], pos):
            return True
        elif move.dx == 1 and check_bit(self.state.con[1], pos):
            return True
        elif move.dy == 1 and check_bit(self.state.con[2], pos):
            return True
        elif move.dx == -1 and check_bit(self.state.con[3], pos):
            return True
        else:
            return False

    def valid_wall(self, new_wall):
        valid = True
        if not self.wall_inbounds(new_wall):
            valid = False
        elif not self.no_wall_overlap(new_wall):
            valid = False
        else:
            self.state.set_wall(new_wall)
            if not self.no_block_in(new_wall):
                valid = False

            self.state.reset_wall(new_wall)

        return valid

    def wall_inbounds(self, new_wall):
        if new_wall.o == "H":
            if new_wall.x >= 8:
                return False
            elif new_wall.y <= 0:
                return False
            elif new_wall.y > 8:
                return False
            elif new_wall.x < 0:
                return False
        else:
            if new_wall.y >= 8:
                return False
            elif new_wall.x <= 0:
                return False
            elif new_wall.y < 0:
                return False
            elif new_wall.x > 8:
                return False

        return True

    def no_wall_overlap(self, new_wall):
        valid = True
        if len(self.state.walls) > 0:
            for w in self.state.walls:
                # idenical walls
                if w.o == new_wall.o and w.x == new_wall.x and w.y == new_wall.y:
                    valid = False
                # new wall 1 above an existing vertical wall
                elif (
                    w.o == "V"
                    and new_wall.o == "V"
                    and w.x == new_wall.x
                    and w.y == new_wall.y + 1
                ):
                    valid = False
                # new wall 1 below an existing vertical wall
                elif (
                    w.o == "V"
                    and new_wall.o == "V"
                    and w.x == new_wall.x
                    and w.y == new_wall.y - 1
                ):
                    valid = False
                # new wall 1 to the left of a horizonal wall
                elif (
                    w.o == "H"
                    and new_wall.o == "H"
                    and w.x == new_wall.x - 1
                    and w.y == new_wall.y
                ):
                    valid = False
                # new wall 1 to the right of a horizonal wall
                elif (
                    w.o == "H"
                    and new_wall.o == "H"
                    and w.x == new_wall.x + 1
                    and w.y == new_wall.y
                ):
                    valid = False
                # new vertical wall crossing a horizontal
                elif (
                    w.o == "H"
                    and new_wall.o == "V"
                    and w.x == new_wall.x - 1
                    and w.y == new_wall.y + 1
                ):
                    valid = False
                # new Horizontal wall crossing a vertical
                elif (
                    w.o == "V"
                    and new_wall.o == "H"
                    and w.x == new_wall.x + 1
                    and w.y == new_wall.y - 1
                ):
                    valid = False

        return valid

    def no_block_in(self, new_wall):
        valid = True
        for pl in self.state.players:
            if pl.position.x != -1 and self.get_path_len(pl) == -11:
                valid = False

        return valid

    def get_path_len(self, pl):
        pos = self.state.pl_pos[pl.index]
        # make sure the person is still playing
        if pos > -1:
            # check for win condition
            if check_bit(self.pl_won[pl.index], pos):
                return -1
            self.depth = +1
            win = self.pl_won[pl.index]
            cur = 1 << pos
            visits = cur
            dist = 0
            while True:
                if cur == 0:
                    # no valid path
                    return -11

                if (cur & win) > 0:
                    return dist

                cur = (
                    (cur & self.state.con[0]) >> 9
                    | (cur & self.state.con[1]) << 1
                    | (cur & self.state.con[2]) << 9
                    | (cur & self.state.con[3]) >> 1
                )
                cur &= ~visits
                visits |= cur
                dist += 1
        # player is already eliminated
        return -111

    # This is the minimax function. It considers all
    # the possible ways the game can go and returns
    # the value of the board
    def minimax(self, depth: int, player):
        max_depth = 1
        score = g.game_score(player)

        isMax = False
        if player.index == my_id:
            isMax = True
        # If Maximizer has won the game return his/her
        # evaluated score
        if score >= 100000:
            return score

        # If Minimizer has won the game return his/her
        # evaluated score
        if score <= -100000:
            return score

        if depth == max_depth:
            # print("score from minimax is:"+str(score), file=sys.stderr, flush=True)
            return score

        # If this maximizer's move
        if isMax:
            best = -100000

            # Traverse all move options
            for t in best_turns(player):
                # Check if t is valid
                if is_valid_turn(t, player):
                    # Make the move
                    g.state.take_turn(player, t)
                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(
                        best,
                        self.minimax(
                            depth + 1,
                            g.state.players[(player.index + 1) % player_count],
                        ),
                    )

                    # Undo the move
                    g.state.undo_turn(player, t)
            return best

        # If this minimizer's move
        else:
            best = 10000

            # Traverse all move options
            for t in best_turns(player):
                # Check if t is valid
                if is_valid_turn(t, player):
                    # Make the move
                    g.state.take_turn(player, t)
                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(
                        best,
                        self.minimax(
                            depth + 1,
                            g.state.players[(player.index + 1) % player_count],
                        ),
                    )

                    # Undo the move
                    g.state.undo_turn(player, t)
            return best

    # This will return the best possible move for the player
    def findBestMove(self, player):
        bestVal: int = -1000000
        bestMove = -1

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for t in best_turns(player):
            # Check if t is valid

            if is_valid_turn(t, player):
                # Make the move
                g.state.take_turn(player, t)
                # compute evaluation function for this
                # move.
                moveVal = self.minimax(
                    0, g.state.players[(player.index + 1) % player_count]
                )

                # Undo the move
                g.state.undo_turn(player, t)

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if moveVal > bestVal:
                    bestMove = t
                    bestVal = moveVal
        return bestMove

    def game_score(self, player):
        a = -1
        b = 1
        c = 1
        d = -1
        e = -1
        gscore = 0
        oppo_dist = 0
        pl_dist = 0
        for pl in self.state.players:
            dist = self.get_path_len(pl)

            if pl.index != my_id and dist == -1:
                # opponnent wins
                gscore += -100000
                break
            if pl.index == my_id and dist == -1:
                # player wins
                gscore += 100000
            if pl.index != my_id and dist == -11:
                # oppo made a blocking move, player wins

                gscore += 100000
                break
            if pl.index == my_id and dist == -11:
                # player made a blocking move, oppo wins
                gscore += -100000

            if pl.index == my_id:
                pl_dist = dist

            elif pl.walls != -1:
                oppo_dist += dist

        # add a * the difference in length of path to victory for the best opponent
        # print("gscore 1 is:"+str(gscore), file=sys.stderr, flush=True)
        gscore += a * pl_dist
        # print("gscore 2 is:"+str(gscore), file=sys.stderr, flush=True)
        # print("oppo dist is:"+str(oppo_dist), file=sys.stderr, flush=True)
        gscore += b * (oppo_dist / (player_count - 1))
        # score += c * pl.walls
        # score += d * min(oppo_walls)
        # score += e * self.walls_ahead(pl)
        # print("gscore 3 is:"+str(gscore), file=sys.stderr, flush=True)
        return gscore


class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __repr__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class move:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return "[" + str(self.dx) + "," + str(self.dy) + "]"

    def __repr__(self):
        return "[" + str(self.dx) + "," + str(self.dy) + "]"

    def __eq__(self, other):
        return self.dx == other.dx and self.dy == other.dy

    def __hash__(self) -> int:
        return hash(self.dx + (10 * self.dy))


class cell:
    def __init__(self, position, data=None, valid_moves: list[position] = []):
        self.position = position
        self.data = data
        self.valid_moves = valid_moves

    def __str__(self):
        return str(self.position) + ":" + str(self.data)


class grid:
    def __init__(self, w: int, h: int, cells: list[cell] = []):
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
        self.cells = numpy.empty((w, h), "object")
        for i in range(w):
            for j in range(h):
                self.cells[i][j] = cell(i, j)

    # how do we score a grid


class player:
    def __init__(self, index, position, board, walls=0):
        self.index = index
        self.position = position
        self.walls = walls  # number of wall elements left
        self.win = []  # list of positions that constitute winning the game
        self.board = board

    def __str__(self):
        return "[" + str(self.index) + " @ " + str(self.position) + "]"

    def __repr__(self):
        return "[" + str(self.index) + " @ " + str(self.position) + "]"

    def __eq__(self, other):
        return self.index == other.index and self.board == other.board

    # identify positions that count as a win if this player is on them
    def add_winning_position(self, position):
        self.win.append(position)

    def move(self, m):
        self.position.x += m.dx
        self.position.y += m.dy

    def move_back(self, m):
        self.position.x -= m.dx
        self.position.y -= m.dy

    def won(self):
        if self.position in self.win:
            return True
        else:
            return False

    def all_turns(self):
        turns = []
        turns.append(move(0, -1))
        turns.append(move(0, 1))
        turns.append(move(1, 0))
        turns.append(move(-1, 0))
        for i in range(9):
            for j in range(9):
                for k in ["V", "H"]:
                    turns.append(wall(i, j, k))
        return turns


class wall:
    def __init__(self, x, y, o):
        self.x = x
        self.y = y
        self.o = o

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "," + str(self.o) + "]"

    def __repr__(self):
        return "[" + str(self.x) + "," + str(self.y) + "," + str(self.o) + "]"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.o == other.o

    def __hash__(self) -> int:
        return hash(self.__str__())

    def to_text(self):
        return self.__str__()


# game function not linked to a specific class


# convert list of moves to text for the output
def route_to_moves(route):
    current = route.pop(0)
    moves = []
    for i in route:
        dx = i.x - current.x
        dy = i.y - current.y
        if dx == 0 and dy == 1:
            moves.append("DOWN")
        elif dx == 0 and dy == -1:
            moves.append("UP")
        elif dx == 1 and dy == 0:
            moves.append("RIGHT")
        elif dx == -1 and dy == 0:
            moves.append("LEFT")
        else:
            moves.append("????")
        current.x = i.x
        current.y = i.y
    return moves


def turn_to_text(t):
    if isinstance(t, move):
        if t.dx == 0 and t.dy == 1:
            return "DOWN"
        elif t.dx == 0 and t.dy == -1:
            return "UP"
        elif t.dx == 1:
            return "RIGHT"
        elif t.dx == -1:
            return "LEFT"
    elif isinstance(t, wall):
        return str(t.x) + " " + str(t.y) + " " + str(t.o)


def text_to_wall(t):
    return wall(int(t[0]), int(t[2]), t[4])


def text_to_turn(t):
    turn = None
    if t == "DOWN":
        turn = move(0, 1)
    elif t == "UP":
        turn = move(0, -1)
    elif t == "LEFT":
        turn = move(-1, 0)
    elif t == "RIGHT":
        turn = move(1, 0)
    else:
        turn = text_to_wall(t)

    return turn


def is_valid_turn(t, p: player):
    if isinstance(t, wall):
        return g.valid_wall(t)
    if isinstance(t, move):
        return g.valid_move(p.position, t)
    if isinstance(t, str):
        return is_valid_turn(text_to_turn(t), p)


def best_turns(player):
    turns = []
    turns.append(move(0, -1))
    turns.append(move(0, 1))
    turns.append(move(1, 0))
    turns.append(move(-1, 0))
    if player.walls:
        turns.extend(g.state.touching_walls())
        # turns.extend(g.state.touching_players())

    unique_turns = list(set(turns))

    return unique_turns


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
strategy_78 = ["1 7 H", "3 7 H", "LEFT", "5 7 H", "BEST", "7 7 V"]
strategy_01 = ["1 2 H", "3 2 H", "LEFT", "5 2 H", "BEST", "7 0 V"]

strategy_78L = ["6 7 H", "4 7 H", "RIGHT", "2 7 H", "BEST", "1 7 V", "BEST", "0 7 H"]
strategy_01L = ["6 2 H", "4 2 H", "RIGHT", "2 2 H", "BEST", "1 0 V", "BEST", "0 2 H"]

strategy_3L = [
    "RIGHT",
    "1 1 V",
    "1 5 V",
    "1 1 H",
    "3 1 H",
    "5 1 H",
    "BEST",
    "BEST",
    "1 3 V",
]
strategy_3 = [
    "8 1 V",
    "8 5 V",
    "6 1 H",
    "4 1 H",
    "2 1 H",
    "BEST",
    "8 3 V",
    "BEST",
    "BEST",
]

strategy_45 = [
    "LEFT",
    "8 6 V",
    "8 2 V",
    "6 8 H",
    "4 8 H",
    "2 8 H",
    "8 4 V",
    "BEST",
    "BEST",
    "8 0 V",
]
strategy_45L = [
    "RIGHT",
    "1 6 V",
    "1 2 V",
    "1 8 H",
    "3 8 H",
    "5 8 H",
    "1 4 V",
    "BEST",
    "BEST",
    "1 0 V",
]

strategy_p0 = ["0 1 H", "2 1 H", "4 1 H", "6 1 H", "RIGHT", "RIGHT", "RIGHT", "RIGHT"]
# game loop
while True:
    # measure the time at the start of a loop

    game_turn += 1
    players = []
    walls = []
    output = ""

    g = game()

    # get turn data from standard input stream
    for i in range(player_count):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # walls_left: number of walls available for the player
        x, y, walls_left = [int(j) for j in input().split()]
        g.add_player(player(i, position(x, y), g, walls_left))

    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        inputs = input().split()
        wall_x = int(inputs[0])  # x-coordinate of the wall
        wall_y = int(inputs[1])  # y-coordinate of the wall
        wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
        g.state.set_wall(wall(wall_x, wall_y, wall_orientation))

    start = time.process_time()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # print("map.players = "+ str(map.players), file=sys.stderr, flush=True)

    # choose oppo
    # TODO possible choose the oppo dynamically

    if player_count == 3:
        oppo_dist = 0
        for pl in g.state.players:
            if pl.index != my_id:
                new_oppo_dist = g.get_path_len(pl)
                if new_oppo_dist > oppo_dist:
                    oppo_dist = new_oppo_dist
                    oppo_id = pl.index
    else:
        if my_id == 0:
            oppo_id = 1
        if my_id == 1:
            oppo_id = 0

    me = g.state.players[my_id]

    oppo = g.state.players[oppo_id]

    # setup for each turn

    if game_turn < 2 and player_count == 2:
        if oppo.position in [
            position(1, 7),
            position(1, 8),
            position(0, 7),
            position(0, 8),
        ]:
            strategy = strategy_78
        if oppo.position in [
            position(1, 1),
            position(1, 0),
            position(0, 0),
            position(0, 1),
        ]:
            strategy = strategy_01
        if oppo.position in [position(8, 1), position(8, 0)]:
            strategy = strategy_01L
        if oppo.position in [position(8, 7), position(8, 8)]:
            strategy = strategy_78L
        if oppo.position in [position(8, 4), position(8, 5)]:
            strategy = strategy_45L
        if oppo.position in [
            position(1, 4),
            position(0, 4),
            position(1, 5),
            position(0, 5),
        ]:
            strategy = strategy_45
        if oppo.position in [position(8, 3)]:
            strategy = strategy_3L
        if oppo.position in [position(0, 3), position(1, 3)]:
            strategy = strategy_3
        # if me.position in [position(0,0)]: strategy = "p0"

    if strategy:
        if strategy[0] == "BEST":
            strategy[0] = turn_to_text(g.findBestMove(me))
        if is_valid_turn(strategy[0], me):
            output = strategy.pop(0)
        else:
            strategy = ""

    if strategy == "" or output == "":
        output = turn_to_text(g.findBestMove(me))
    end = time.process_time() - start
    print("time taken = " + str(end), file=sys.stderr, flush=True)

    print(output)
