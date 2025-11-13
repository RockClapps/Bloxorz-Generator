from enum import Enum
import random as rand
from copy import deepcopy

# Maximum size of board/grid space
max_x = 20
max_y = 20

# Positiion(vertical) that player block starts in
start_x = int(max_x/2)
start_y = int(max_y/2)

# How many moves it should generate
total_moves = 20

floor = 'XX'
initial_state = 'II'
goal_state = 'GG'

class Blox:
    # Player block object. Keeps track of orientation
    class Orientation(Enum):
        STAND = 0
        VERT = 1
        HOR = 2

    orientation = Orientation.STAND

    def move_vert(self):
        if self.orientation == self.Orientation.STAND:
            self.orientation = self.Orientation.VERT
        elif self.orientation == self.Orientation.VERT:
            self.orientation = self.Orientation.STAND

    def move_hor(self):
        if self.orientation == self.Orientation.STAND:
            self.orientation = self.Orientation.HOR
        elif self.orientation == self.Orientation.HOR:
            self.orientation = self.Orientation.STAND


class PositionTracker:
    # Tracks the current block position, as well as the highest, lowest, left-most,
    # and right-most squares covered by the block at the current time for easy
    # assessment.

    positions = []
    highest_position = ()
    lowest_position = ()
    leftest_position = ()
    rightest_position = ()

    def __init__(self, starting_positions):
        # Take a list of touples that the blox is on
        self.updatePositions(starting_positions)

    def updatePositions(self, new_positions):
        # Given a new set of positions, calculate the new highest,lowest, left-most,
        # and right-most board spaces. Also sort positions for consistancy and
        # serializability
        self.positions = deepcopy(new_positions)
        highest = self.positions[0]
        lowest = self.positions[0]
        leftest = self.positions[0]
        rightest = self.positions[0]
        for x in self.positions:
            if x[0] < highest[0]:
                highest = x
            if x[0] > lowest[0]:
                lowest = x
            if x[1] < leftest[1]:
                leftest = x
            if x[1] > rightest[1]:
                rightest = x
        self.highest_position = highest
        self.lowest_position = lowest
        self.leftest_position = leftest
        self.rightest_position = rightest
        self.positions.sort()


class Game:
    # Starts with a Blox object, an empty grid, a position tracker, a states variable
    # that keeps track of all previous grid states and positions, and a solution that
    # is not necessarily the most efficient

    blox = Blox()
    grid = []
    positionTracker = PositionTracker([(start_x, start_y)])
    states = []
    solution = []

    class Moves(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self):
        # Resets every variable so that you can run multiple generations in a row
        self.blox = Blox()
        self.grid = []
        self.positionTracker = PositionTracker([(start_x, start_y)])
        self.states = []
        self.solution = []
        for i in range(max_y):
            self.grid.append([])
            for j in range(max_x):
                self.grid[i].append("  ")
        self.grid[start_x][start_y] = initial_state
        self.trackState(None)

    def trackState(self, move):
        # Recordes the latest move and current state
        self.solution.append(move)
        self.states.append(
            (deepcopy(self.grid), deepcopy(self.positionTracker.positions)))

    def condenseStates(self):
        # If the blox rolls onto a space that it has been to previously, delete all
        # activity between the previous state and the new one. This can be modified
        # easily in the future to account for full board states like if you pressed a
        # button

        if len(self.states) == 0:
            return -1
        currentstate = self.states[-1]
        for i in range(len(self.states)-2, -1, -1):
            if self.states[i][1] == currentstate[1]:
                self.states = self.states[0:i+1]
                self.solution = self.solution[0:i+1]
                self.grid = deepcopy(self.states[i][0])
                return

    def scoreGrid(self):
        # Basic way to score a given problem, just divides length of solution by
        # spaces on the board
        spaces = 0
        moves = len(self.solution)
        for x in self.grid:
            for y in x:
                if y != '':
                    spaces += 1
        return moves / spaces

    def printGrid(self, grid=None):
        # Prints the problem grid in the required machine readable format
        if grid is None:
            grid = self.grid
        for x in grid:
            line = ''
            for y in x:
                line += y
            print(line)

    def printGridVisual(self, grid=None):
        # Prints the problem grid in a more human readable format. Includes solution
        # list and score
        if grid is None:
            grid = self.grid
        for x in grid:
            line = ''
            for y in x:
                line += y[0]
            print(line)
        print(self.solution)
        print(self.scoreGrid())

    # The move_DIRECTION functions below use the position tracker and the blox object
    # to figure out what spaces the blox will cover if it moves from its current
    # position. If the move is illegal (like moving past the maximum map size), it
    # returns false
    def move_up(self):
        highest = self.positionTracker.highest_position
        leftest = self.positionTracker.leftest_position
        rightest = self.positionTracker.rightest_position
        if highest[0] < 2:
            return False
        self.blox.move_vert()
        newPositions = []
        if self.blox.orientation == self.blox.Orientation.STAND:
            newPositions = [
                (highest[0] - 1, highest[1]),
            ]
        if self.blox.orientation == self.blox.Orientation.VERT:
            newPositions = [
                (highest[0] - 1, highest[1]),
                (highest[0] - 2, highest[1]),
            ]
        if self.blox.orientation == self.blox.Orientation.HOR:
            newPositions = [
                (leftest[0] - 1, leftest[1]),
                (rightest[0] - 1, rightest[1]),
            ]
        self.positionTracker.updatePositions(newPositions)
        return True

    def move_down(self):
        lowest = self.positionTracker.lowest_position
        leftest = self.positionTracker.leftest_position
        rightest = self.positionTracker.rightest_position
        if lowest[0] >= max_x - 2:
            return False
        self.blox.move_vert()
        newPositions = []
        if self.blox.orientation == self.blox.Orientation.STAND:
            newPositions = [
                (lowest[0] + 1, lowest[1]),
            ]
        if self.blox.orientation == self.blox.Orientation.VERT:
            newPositions = [
                (lowest[0] + 1, lowest[1]),
                (lowest[0] + 2, lowest[1]),
            ]
        if self.blox.orientation == self.blox.Orientation.HOR:
            newPositions = [
                (leftest[0] + 1, leftest[1]),
                (rightest[0] + 1, rightest[1]),
            ]
        self.positionTracker.updatePositions(newPositions)
        return True

    def move_left(self):
        leftest = self.positionTracker.leftest_position
        lowest = self.positionTracker.lowest_position
        highest = self.positionTracker.highest_position
        if leftest[1] < 2:
            return False
        self.blox.move_hor()
        newPositions = []
        if self.blox.orientation == self.blox.Orientation.STAND:
            newPositions = [
                (leftest[0], leftest[1] - 1),
            ]
        if self.blox.orientation == self.blox.Orientation.VERT:
            newPositions = [
                (lowest[0], lowest[1] - 1),
                (highest[0], highest[1] - 1),
            ]
        if self.blox.orientation == self.blox.Orientation.HOR:
            newPositions = [
                (leftest[0], leftest[1] - 1),
                (leftest[0], leftest[1] - 2),
            ]
        self.positionTracker.updatePositions(newPositions)
        return True

    def move_right(self):
        rightest = self.positionTracker.rightest_position
        lowest = self.positionTracker.lowest_position
        highest = self.positionTracker.highest_position
        if rightest[1] >= max_x - 2:
            return False
        self.blox.move_hor()
        newPositions = []
        if self.blox.orientation == self.blox.Orientation.STAND:
            newPositions = [
                (rightest[0], rightest[1] + 1),
            ]
        if self.blox.orientation == self.blox.Orientation.VERT:
            newPositions = [
                (lowest[0], lowest[1] + 1),
                (highest[0], highest[1] + 1),
            ]
        if self.blox.orientation == self.blox.Orientation.HOR:
            newPositions = [
                (rightest[0], rightest[1] + 1),
                (rightest[0], rightest[1] + 2),
            ]
        self.positionTracker.updatePositions(newPositions)
        return True

    def generateMap(self, total_moves, requireStand=False):
        # Generates a complete problem given a minimum number of moves explored. It
        # randomly picks a move to do, executes it, and records ground where the
        # block fell. This function also tracks the moves and uses condenseStates()
        # to clean up duplicated states
        for i in range(total_moves):
            move = self.Moves(rand.randint(0, 3))
            success = False
            if move == self.Moves.UP:
                success = self.move_up()
            if move == self.Moves.DOWN:
                success = self.move_down()
            if move == self.Moves.LEFT:
                success = self.move_left()
            if move == self.Moves.RIGHT:
                success = self.move_right()
            if success:
                for p in self.positionTracker.positions:
                    self.grid[p[0]][p[1]] = floor
                self.trackState(move)
                self.condenseStates()
        if requireStand and self.blox.orientation != self.blox.Orientation.STAND:
            return self.generateMap(1, requireStand)

        self.grid[start_x][start_y] = initial_state
        for p in self.positionTracker.positions:
            self.grid[p[0]][p[1]] = goal_state


# Generate 100 problems and print the ones with a score over 0.025
for i in range(100):
    game = Game()
    game.generateMap(total_moves, requireStand=True)
    if game.scoreGrid() >= .045:
        game.printGridVisual()

# for x in game.states:
#    game.printGridVisual(x[0])

# TODO implement problem grading based on high number of actions and few number
# of spaces
