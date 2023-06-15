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

    def set_wall(self, wall):
        pos = wall.x + (wall.y * w)
        type = wall.o
        if type == "H":
            self.con[0] = reset_bit(self.con[0], pos)
            self.con[0] = reset_bit(self.con[0], pos + 1)
            self.con[2] = reset_bit(self.con[2], pos - w)
            self.con[2] = reset_bit(self.con[2], pos - w + 1)
        else:
            self.con[1] = reset_bit(self.con[1], pos - 1)
            self.con[1] = reset_bit(self.con[1], pos + w - 1)
            self.con[3] = reset_bit(self.con[3], pos)
            self.con[3] = reset_bit(self.con[3], pos + w)
        self.walls.append(wall)

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
            print("wall out of bounbds", file=sys.stderr, flush=True)
        elif not self.no_wall_overlap(new_wall):
            valid = False
            print("wall overlap", file=sys.stderr, flush=True)
        else:
            self.state.set_wall(new_wall)
            if not self.no_block_in(new_wall):
                valid = False
                print("wall causes block in", file=sys.stderr, flush=True)
            self.state.reset_wall(new_wall)

        return valid

    def wall_inbounds(self, new_wall):
        valid = True
        if new_wall.o == "H" and new_wall.x >= 8:
            valid = False
        elif new_wall.o == "H" and new_wall.y <= 0:
            valid = False
        elif new_wall.o == "H" and new_wall.y > 8:
            valid = False
        elif new_wall.o == "H" and new_wall.x < 0:
            valid = False
        elif new_wall.o == "V" and new_wall.y >= 8:
            valid = False
        elif new_wall.o == "V" and new_wall.x <= 0:
            valid = False
        elif new_wall.o == "V" and new_wall.y < 0:
            valid = False
        elif new_wall.o == "V" and new_wall.x > 8:
            valid = False

        return valid

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
        print(
            "pos of: " + str(pl.index) + " = " + str(pos), file=sys.stderr, flush=True
        )
        # make sure the person is still playing
        if pos > -1:
            # check for win condition
            if check_bit(self.pl_won[pl.index], pos):
                print(str(bin(self.pl_won[pl.index])), file=sys.stderr, flush=True)
                return -1
            self.depth = +1
            win = self.pl_won[pl.index]
            cur = 1 << pos
            visits = cur
            dist = 0
            while True:
                if cur == 0:
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
        return -111

    def best_move(self, player):
        best_score = -10000
        best_move = None

        for t in best_turns(player):
            print("", file=sys.stderr, flush=True)
            print("move: " + str(t), file=sys.stderr, flush=True)
            if is_valid_turn(t, player):
                print("Valid turn", file=sys.stderr, flush=True)
                if isinstance(t, wall):
                    g.state.set_wall(t)
                    new_score = g.game_score(me)
                    print("score: " + str(new_score), file=sys.stderr, flush=True)
                    if new_score > best_score:
                        best_score = new_score
                        best_move = t
                    g.state.reset_wall(t)
                if isinstance(t, move):
                    g.state.move_player(player, t)
                    new_score = g.game_score(me)
                    print("score: " + str(new_score), file=sys.stderr, flush=True)
                    if new_score > best_score:
                        best_score = new_score
                        best_move = t
                    g.state.unmove_player(player, t)
            else:
                print("not valid turn", file=sys.stderr, flush=True)

        return best_move

    def game_score(self, pl):
        a = -5
        b = 5
        c = 1
        d = -1
        e = -1
        score = 0
        oppo_dist = 100
        pl_dist = 100
        for pl in self.state.players:
            dist = self.get_path_len(pl)
            if pl.index != my_id and dist == -1:
                # opponnent wins
                print("player has won", file=sys.stderr, flush=True)
                score += -111111
                break
            if pl.index == my_id and dist == -1:
                # I win
                print("I have win", file=sys.stderr, flush=True)
                score += 99999999
            if dist == -11:
                # no valid moves
                print("no valid path", file=sys.stderr, flush=True)
                score += -22222
                break
            if pl.index == my_id:
                pl_dist = dist
                print("pl dist = : " + str(pl_dist), file=sys.stderr, flush=True)
            elif pl.walls != -1:
                oppo_dist += dist
                print("oppo dist = : " + str(oppo_dist), file=sys.stderr, flush=True)

        # add a * the difference in length of path to victory for the best opponent
        score += a * pl_dist
        score += b * (oppo_dist / (player_count - 1))
        # score += c * pl.walls
        # score += d * min(oppo_walls)
        # score += e * self.walls_ahead(pl)
        # print("score after that move is"+ str(score), file=sys.stderr, flush=True)
        return score


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

    def add_wall(self, new_wall):
        if new_wall not in self.walls:
            self.walls.append(new_wall)

            self.set_valid_neighbours(position(new_wall.x, new_wall.y))
            if new_wall.o == "V":
                self.set_valid_neighbours(position(new_wall.x - 1, new_wall.y))
                self.set_valid_neighbours(position(new_wall.x - 1, new_wall.y + 1))
                self.set_valid_neighbours(position(new_wall.x, new_wall.y + 1))
            else:
                self.set_valid_neighbours(position(new_wall.x, new_wall.y - 1))
                self.set_valid_neighbours(position(new_wall.x + 1, new_wall.y - 1))
                self.set_valid_neighbours(position(new_wall.x + 1, new_wall.y))

    def remove_wall(self, old_wall):
        if old_wall in self.walls:
            self.walls.remove(old_wall)
            self.set_valid_neighbours(position(old_wall.x, old_wall.y))
            if old_wall.o == "V":
                self.set_valid_neighbours(position(old_wall.x - 1, old_wall.y))
                self.set_valid_neighbours(position(old_wall.x - 1, old_wall.y + 1))
                self.set_valid_neighbours(position(old_wall.x, old_wall.y + 1))
            else:
                self.set_valid_neighbours(position(old_wall.x, old_wall.y - 1))
                self.set_valid_neighbours(position(old_wall.x + 1, old_wall.y - 1))
                self.set_valid_neighbours(position(old_wall.x + 1, old_wall.y))

    def add_player(self, index, pos, player_data):
        # create a player with reference back to this board
        self.players.append(player(index, pos, self, player_data))

    def move_player(self, i, m):
        self.players[i].move(m)

    def move_player_back(self, i, m):
        self.players[i].move_back(m)

    # how do we score a grid
    def grid_score(self, pl):
        a = -5
        b = 5
        c = 1
        d = -1
        e = -1
        score = 0
        oppo_dist = 100
        path = []
        pl_dist = 100
        for pl in self.players:
            dist = pl.moves_to_victory()
            if dist == -1:
                # wall causes a block in
                score += -10000
                break
            if pl.index == my_id:
                pl_dist = dist
            elif len(path) < oppo_dist:
                oppo_dist = dist

        # add a * the difference in length of path to victory for the best opponent
        score += a * pl_dist
        score += b * (oppo_dist - 1)
        # score += c * pl.walls
        # score += d * min(oppo_walls)
        # score += e * self.walls_ahead(pl)
        # print("score after that move is"+ str(score), file=sys.stderr, flush=True)
        return score

    def walls_ahead(self, pl):
        wa = 0
        for w in self.walls:
            if pl.index == 0:
                if w.x > pl.position.x:
                    wa += 1
            if pl.index == 1:
                if w.x < pl.position.x:
                    wa += 1
            if pl.index == 2:
                if w.y > pl.position.y:
                    wa += 1
        return wa

    def walls_behind(self, pl):
        w = 0
        for w in self.walls:
            if pl.index == 0:
                if w.x < pl.position.x:
                    wb += 1
            if pl.index == 1:
                if w.x > pl.position.x:
                    wb += 1
            if pl.index == 2:
                if w.y < pl.position.y:
                    wb += 1
        return wb

    def won_by(self):
        winner = None
        for p in self.players:
            if p.won():
                winner = p
        return winner

    def astar(self, start):
        pass

    # for a given position is a move valid
    def valid_move(self, position, move):
        valid = True
        # is the moved blocked by a wall
        if len(self.walls) < 1:
            for w in self.walls:
                if (
                    w.o == "V"
                    and move.dx == 1
                    and w.x == position.x + 1
                    and (w.y == position.y or w.y + 1 == position.y)
                ):
                    return False
                elif (
                    w.o == "V"
                    and move.dx == -1
                    and w.x == position.x
                    and (w.y == position.y or w.y + 1 == position.y)
                ):
                    return False
                elif (
                    w.o == "H"
                    and move.dy == 1
                    and w.y == position.y + 1
                    and (w.x == position.x or w.x + 1 == position.x)
                ):
                    return False
                elif (
                    w.o == "H"
                    and move.dy == -1
                    and w.y == position.y
                    and (w.x == position.x or w.x + 1 == position.x)
                ):
                    return False
        else:
            print("walls :" + str(self.walls), file=sys.stderr, flush=True)
            print(
                " is [2,0,V] in walls" + str(wall(2, 0, "V") in self.walls),
                file=sys.stderr,
                flush=True,
            )
            if move.dx == 1 and (
                wall(position.x + 1, position.y, "H") in self.walls
                or (wall(position.x + 1, position.y - 1, "V") in self.walls)
            ):
                return False
            if move.dx == -1 and (
                wall(position.x, position.y, "H") in self.walls
                or (wall(position.x, position.y - 1, "V") in self.walls)
            ):
                return False
            if move.dy == 1 and (
                wall(position.x, position.y + 1, "H") in self.walls
                or (wall(position.x - 1, position.y + 1, "H") in self.walls)
            ):
                return False
            if move.dy == -1 and (
                wall(position.x, position.y, "H") in self.walls
                or (wall(position.x - 1, position.y, "H") in self.walls)
            ):
                return False

        # does the move take you out of bounds
        if position.x + move.dx > 8:
            return False
        if position.x + move.dx < 0:
            return False
        if position.y + move.dy > 8:
            return False
        if position.y + move.dy < 0:
            return False

        return valid

    def valid_move2(self, po, move):
        if (
            position(po.x + move.dx, po.y + move.dy)
            in self.cells[po.x][po.y].valid_moves
        ):
            return True
        else:
            return False

    # is it valid to place another wall with orintation on this grid
    def valid_wall(self, new_wall):
        valid = True
        valid = self.wall_inbounds(new_wall)
        if valid:
            valid = self.no_wall_overlap(new_wall)
        # if valid:
        #    self.add_wall(new_wall)
        #    valid = self.no_block_in(new_wall)
        #    self.remove_wall(new_wall)
        return valid

    def wall_inbounds(self, new_wall):
        valid = True
        if new_wall.o == "H" and new_wall.x >= 8:
            valid = False
        elif new_wall.o == "H" and new_wall.y <= 0:
            valid = False
        elif new_wall.o == "H" and new_wall.y > 8:
            valid = False
        elif new_wall.o == "H" and new_wall.x < 0:
            valid = False
        elif new_wall.o == "V" and new_wall.y >= 8:
            valid = False
        elif new_wall.o == "V" and new_wall.x <= 0:
            valid = False
        elif new_wall.o == "V" and new_wall.y < 0:
            valid = False
        elif new_wall.o == "V" and new_wall.x > 8:
            valid = False

        return valid

    def no_wall_overlap(self, new_wall):
        valid = True
        if len(walls) > 0:
            for w in walls:
                # idenical walls
                if w.o == new_wall.o and w.x == new_wall.x and w.y == new_wall.y:
                    valid = False
                # new wall 1 below an existing vertical wall
                elif (
                    w.o == "V"
                    and new_wall.o == "V"
                    and w.x == new_wall.x
                    and w.y == new_wall.y + 1
                ):
                    valid = False
                # new wall 1 above an existing vertical wall
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
        for pl in self.players:
            if pl.position.x != -1 and pl.moves_to_victory() == -1:
                valid = False

        return valid

    def not_out_of_bounds(self, po, mo):
        # does the move take you out of bounds
        if po.x + mo.dx > self.w - 1:
            return False
        if po.x + mo.dx < 0:
            return False
        if po.y + mo.dy > self.h - 1:
            return False
        if po.y + mo.dy < 0:
            return False
        return True

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

    def set_valid_neighbours(self, p=None):
        # add a list of moves accessible cells from all position or just one if specified from position p

        if not p:
            for i in range(h):
                for j in range(w):
                    p = position(j, i)
                    self.cells[p.x][p.y].valid_moves = []
                    # is up valid
                    if self.not_out_of_bounds(p, move(0, -1)):
                        self.cells[p.x][p.y].valid_moves.append(position(p.x, p.y - 1))
                    # is down valid
                    if self.not_out_of_bounds(p, move(0, 1)):
                        self.cells[p.x][p.y].valid_moves.append(position(p.x, p.y + 1))
                    # is left valid
                    if self.not_out_of_bounds(p, move(-1, 0)):
                        self.cells[p.x][p.y].valid_moves.append(position(p.x - 1, p.y))
                    # is right valid
                    if self.not_out_of_bounds(p, move(1, 0)):
                        self.cells[p.x][p.y].valid_moves.append(position(p.x + 1, p.y))
        else:
            self.cells[p.x][p.y].valid_moves = []
            if self.valid_move2(p, move(0, -1)):
                self.cells[p.x][p.y].valid_moves.append(position(p.x, p.y - 1))
            # is down valid
            if self.valid_move2(p, move(0, 1)):
                self.cells[p.x][p.y].valid_moves.append(position(p.x, p.y + 1))
            # is left valid
            if self.valid_move2(p, move(-1, 0)):
                self.cells[p.x][p.y].valid_moves.append(position(p.x - 1, p.y))
            # is right valid
            if self.valid_move2(p, move(1, 0)):
                self.cells[p.x][p.y].valid_moves.append(position(p.x + 1, p.y))

    def get_valid_moves(self, p):
        return self.cells[p.x][p.y].valid_moves

    def get_valid_neighbours(self, p):
        # return a list of positions that are reachable from position p
        neighbours = []
        # is up valid
        if self.valid_move(p, move(0, -1)):
            neighbours.append(position(p.x, p.y - 1))
        # is down valid
        if self.valid_move(p, move(0, 1)):
            neighbours.append(position(p.x, p.y + 1))
        # is left valid
        if self.valid_move(p, move(-1, 0)):
            neighbours.append(position(p.x - 1, p.y))
        # is right valid
        if self.valid_move(p, move(1, 0)):
            neighbours.append(position(p.x + 1, p.y))

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

    def moves_to_victory(self):
        n = 0
        previous_nodes = [self.position]
        queue = [(self.position, n)]
        while queue:
            next_node = queue.pop(0)
            children = self.board.cells[next_node[0].x][next_node[0].y].valid_moves
            for c in children:
                if c in self.win:
                    return next_node[1] + 1  # return current length of path
                if c not in previous_nodes:
                    queue.append((c, next_node[1] + 1))
                    previous_nodes.append(c)
        # no winning path found
        return -1

    def next_move(self):
        for p in map.players:
            # print("p.index self.index"+str(p.index)+","+str(self.index), file=sys.stderr, flush=True)
            moves = route_to_moves(self.path_to_victory())
        return moves[0]

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


def all_turns():
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


def text_to_moves(text):
    return all_turns()[text]


# place a wall to block between to positions
def blocks(current, to):
    blocks = []
    # if movement is up
    if current.x == to.x and current.y > to.y:
        blocks.append(wall(current.x, current.y, "H"))
        blocks.append(wall(current.x - 1, current.y, "H"))
    # if movement is down
    if current.x == to.x and current.y < to.y:
        blocks.append(wall(to.x, to.y, "H"))
        blocks.append(wall(to.x - 1, to.y, "H"))
    # if movement is right
    if current.y == to.y and current.x < to.x:
        blocks.append(wall(to.x, to.y, "V"))
        blocks.append(wall(to.x, to.y - 1, "V"))
    # if movement is left
    if current.y == to.y and current.x > to.x:
        blocks.append(wall(current.x, current.y, "V"))
        blocks.append(wall(current.x, current.y - 1, "V"))

    if not map.valid_wall(blocks[1]):
        blocks.pop(1)
    if not map.valid_wall(blocks[0]):
        blocks.pop(0)

    return blocks


# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
def minimax(grid, depth, player):
    max_depth = 3
    score = grid.grid_score(player)
    isMax = False
    if player.index == my_id:
        isMax = True
    # If Maximizer has won the game return his/her
    # evaluated score
    if score == 1000:
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if score == -1000:
        return score

    if depth == max_depth:
        return score

    # If this maximizer's move
    if isMax:
        best = -10000

        # Traverse all move options
        for t in all_turns():
            # Check if t is valid
            if is_valid_turn(t):
                # Make the move
                grid.take_turn(t, player)
                # Call minimax recursively and choose
                # the maximum value
                best = max(
                    best,
                    minimax(
                        grid, depth + 1, grid.players[player.index + 1 % player_count]
                    ),
                )

                # Undo the move
                grid.undo_turn(t, player)
        return best

    # If this minimizer's move
    else:
        best = 10000

        # Traverse all move options
        for t in all_turns():
            # Check if t is valid
            if is_valid_turn(t):
                # Make the move
                grid.take_turn(t, player)
                # Call minimax recursively and choose
                # the maximum value
                best = min(
                    best,
                    minimax(
                        grid, depth + 1, grid.players[player.index + 1 % player_count]
                    ),
                )

                # Undo the move
                grid.undo_turn(t, player)
        return best


# This will return the best possible move for the player
def findBestMove(grid):
    bestVal = -1000
    bestMove = -1

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for t in all_turns():
        # Check if t is valid
        if is_valid_turn(t):
            # Make the move
            grid.take_turn(t, player)
            # compute evaluation function for this
            # move.
            moveVal = minimax(grid, 0, False)

            # Undo the move
            grid.undo_turn(t, player)

            # If the value of the current move is
            # more than the best value, then update
            # best/
            if moveVal > bestVal:
                bestMove = t
                bestVal = moveVal

    # print("The value of the best Move is :", bestVal)
    # print()
    return bestMove


def is_valid_turn(t, p: player):
    if isinstance(t, str):
        t = text_to_turn(t)
    valid = False
    if isinstance(t, wall):
        valid = g.valid_wall(t)
    if isinstance(t, move):
        valid = g.valid_move(p.position, t)
    return valid


def best_turns(player):
    turns = []
    turns.append(move(0, -1))
    turns.append(move(0, 1))
    turns.append(move(1, 0))
    turns.append(move(-1, 0))
    if player.walls:
        turns.extend(g.state.touching_walls())
        turns.extend(g.state.touching_players())

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
strategy_78 = ["1 7 H", "3 7 H", "LEFT", "5 7 H", "LEFT", "7 7 V"]
strategy_01 = ["1 2 H", "3 2 H", "LEFT", "5 2 H", "LEFT", "7 0 V"]

strategy_78L = ["6 7 H", "4 7 H", "RIGHT", "2 7 H", "RIGHT", "1 7 V", "RIGHT", "0 7 H"]
strategy_01L = ["6 2 H", "4 2 H", "RIGHT", "2 2 H", "RIGHT", "1 0 V", "RIGHT", "0 2 H"]

strategy_3L = [
    "RIGHT",
    "1 1 V",
    "1 5 V",
    "1 1 H",
    "3 1 H",
    "5 1 H",
    "RIGHT",
    "RIGHT",
    "1 3 V",
]
strategy_3 = [
    "8 1 V",
    "8 5 V",
    "6 1 H",
    "4 1 H",
    "2 1 H",
    "LEFT",
    "8 3 V",
    "LEFT",
    "LEFT",
]

strategy_45 = [
    "LEFT",
    "8 6 V",
    "8 2 V",
    "6 8 H",
    "4 8 H",
    "2 8 H",
    "8 4 V",
    "LEFT",
    "LEFT",
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
    "RIGHT",
    "RIGHT",
    "1 0 V",
]

strategy_p0 = ["0 1 H", "2 1 H", "4 1 H", "6 1 H", "RIGHT", "RIGHT", "RIGHT", "RIGHT"]
# game loop
while True:
    # measure the time at the start of a loop
    start = time.process_time()

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
    if game_turn < 3 and player_count == 2:
        if oppo.position in [
            position(1, 7),
            position(1, 8),
            position(0, 7),
            position(0, 8),
        ]:
            strategy = "78"
        if oppo.position in [
            position(1, 1),
            position(1, 0),
            position(0, 0),
            position(0, 1),
        ]:
            strategy = "01"
        if oppo.position in [position(8, 1), position(8, 0)]:
            strategy = "01L"
        if oppo.position in [position(8, 7), position(8, 8)]:
            strategy = "78L"
        if oppo.position in [position(8, 4), position(8, 5)]:
            strategy = "45L"
        if oppo.position in [
            position(1, 4),
            position(0, 4),
            position(1, 5),
            position(0, 5),
        ]:
            strategy = "45"
        if oppo.position in [position(8, 3)]:
            strategy = "3L"
        if oppo.position in [position(0, 3), position(1, 3)]:
            strategy = "3"
        # if me.position in [position(0,0)]: strategy = "p0"

    print("Strategy =" + str(strategy), file=sys.stderr, flush=True)

    if strategy == "78":
        if strategy_78:
            if is_valid_turn(strategy_78[0], me):
                output = strategy_78.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "01":
        if strategy_01:
            if is_valid_turn(strategy_01[0], me):
                output = strategy_01.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""
    if strategy == "78L":
        if strategy_78L:
            if is_valid_turn(strategy_78L[0], me):
                output = strategy_78L.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""
    if strategy == "01L":
        if strategy_01L:
            if is_valid_turn(strategy_01L[0], me):
                output = strategy_01L.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "45":
        if strategy_45:
            if is_valid_turn(strategy_45[0], me):
                output = strategy_45.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "45L":
        if strategy_45L:
            if is_valid_turn(strategy_45L[0], me):
                if strategy_45L[0] == "BEST":
                    output = turn_to_text(g.best_move(me))
                else:
                    output = strategy_45L.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "3L":
        if strategy_3L:
            if is_valid_turn(strategy_3L[0], me):
                if strategy_3L[0] == "BEST":
                    output = turn_to_text(g.best_move(me))
                else:
                    output = strategy_3L.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "3":
        if strategy_3:
            if is_valid_turn(strategy_3[0], me):
                if strategy_3[0] == "BEST":
                    output = turn_to_text(g.best_move(me))
                else:
                    output = strategy_3.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "p0":
        if strategy_p0:
            if is_valid_turn(strategy_p0[0], me):
                if strategy_p0[0] == "BEST":
                    output = turn_to_text(g.best_move(me))
                else:
                    output = strategy_p0.pop(0)
            else:
                strategy = ""
        else:
            strategy = ""

    if strategy == "" or output == "":
        print("UP", file=sys.stderr, flush=True)
        for i in range(0, 81, 9):
            print(
                str(bin(g.state.con[0]))[-i - 1 : -i - 10 : -1],
                end=" ",
                file=sys.stderr,
                flush=True,
            )
            print("", file=sys.stderr, flush=True)
        print("RIGHT", file=sys.stderr, flush=True)
        for i in range(0, 81, 9):
            print(
                str(bin(g.state.con[1]))[-i - 1 : -i - 10 : -1],
                end=" ",
                file=sys.stderr,
                flush=True,
            )
            print("", file=sys.stderr, flush=True)
        print("DOWN", file=sys.stderr, flush=True)
        for i in range(0, 81, 9):
            print(
                str(bin(g.state.con[2]))[-i - 1 : -i - 10 : -1],
                end=" ",
                file=sys.stderr,
                flush=True,
            )
            print("", file=sys.stderr, flush=True)
        print("LEFT", file=sys.stderr, flush=True)
        for i in range(0, 81, 9):
            print(
                str(bin(g.state.con[3]))[-i - 1 : -i - 10 : -1],
                end=" ",
                file=sys.stderr,
                flush=True,
            )
            print("", file=sys.stderr, flush=True)
        print("", file=sys.stderr, flush=True)

        output = turn_to_text(g.best_move(me))

        ## TODO allow for if you are player 0,1,2 to account for if this should be > or >=

        end = time.process_time() - start
        # print("time for this round"+ str(end), file=sys.stderr, flush=True)

    print(output)
