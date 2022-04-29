#!/usr/bin/python


# Maze Generator
import sys
import csv
from enum import Enum
from graphics import *


# TODO: Add more status configurations
# Enums to represent Status
class Status(Enum):
    SEARCHING = 0
    FOUND = 1

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

# Temporarily we instantiate Agent with a Searching status
class Agent:
    location = ()
    status = Status.SEARCHING
    fitness = 0
    goal_complete_reward = 25

    def __init__(self):
        print()

    def get_location(self):
        return self.location

    def get_status(self):
        return self.status

    def set_location(self, x_pos, y_pos):
        self.location = (x_pos, y_pos)

    def set_status(self, status):
        self.status = status

    def update_fitness(self, fitness):
        self.fitness = self.fitness + fitness

    # If invalid location it simply does not update the agent's position
    def move(self, direction):
        if direction == Direction.NORTH:
            if maze.get_cell(self.location[0], self.location[1] + 1).is_free or \
                    maze.get_cell(self.location[0], self.location[1] + 1).is_entry:
                self.set_location(self.location[0], self.location[1] + 1)
                self.update_fitness(-abs(maze.get_cell(self.location[0], self.location[1] + 1).get_obstruction_cost()))

                # Updates which cell our agent is currently in
                maze.get_cell(self.get_location()[0], self.get_location()[1]).set_contains_agent(False)
                maze.get_cell(self.location[0], self.location[1] + 1).set_contains_agent(True)

                # Checks if we enter a reward state
                if maze.get_cell(self.location[0], self.location[1] + 1).is_entry and maze.agent.get_status() == Status.SEARCHING:
                    self.update_fitness(self.goal_complete_reward)
                    self.set_status(Status.FOUND)
                return

        if direction == Direction.SOUTH:
            if maze.get_cell(self.location[0], self.location[1] - 1).is_free or \
                    maze.get_cell(self.location[0], self.location[1] - 1).is_entry:
                self.set_location(self.location[0], self.location[1] - 1)
                self.update_fitness(-abs(maze.get_cell(self.location[0], self.location[1] - 1).get_obstruction_cost()))

                # Updates which cell our agent is currently in
                maze.get_cell(self.get_location()[0], self.get_location()[1]).set_contains_agent(False)
                maze.get_cell(self.location[0], self.location[1] + 1).set_contains_agent(True)

                # Checks if we enter a reward state
                if maze.get_cell(self.location[0], self.location[1] - 1).is_entry and maze.agent.get_status() == Status.SEARCHING:
                    self.update_fitness(self.goal_complete_reward)
                    self.set_status(Status.FOUND)
                return

        if direction == Direction.EAST:
            if maze.get_cell(self.location[0] + 1, self.location[1]).is_free or \
                    maze.get_cell(self.location[0] + 1, self.location[1]).is_entry:
                self.set_location(self.location[0] + 1, self.location[1])
                self.update_fitness(-abs(maze.get_cell(self.location[0] + 1, self.location[1]).get_obstruction_cost()))

                # Updates which cell our agent is currently in
                maze.get_cell(self.get_location()[0], self.get_location()[1]).set_contains_agent(False)
                maze.get_cell(self.location[0], self.location[1] + 1).set_contains_agent(True)

                # Checks if we enter a reward state
                if maze.get_cell(self.location[0] + 1, self.location[1]).is_entry and maze.agent.get_status() == Status.SEARCHING:
                    self.update_fitness(self.goal_complete_reward)
                    self.set_status(Status.FOUND)
                return

        if direction == Direction.WEST:
            if maze.get_cell(self.location[0] - 1, self.location[1]).is_free or \
                    maze.get_cell(self.location[0] - 1, self.location[1]).is_entry:
                self.set_location(self.location[0] - 1, self.location[1])
                self.update_fitness(-abs(maze.get_cell(self.location[0] - 1, self.location[1]).get_obstruction_cost()))

                # Updates which cell our agent is currently in
                maze.get_cell(self.get_location()[0], self.get_location()[1]).set_contains_agent(False)
                maze.get_cell(self.location[0], self.location[1] + 1).set_contains_agent(True)

                # Checks if we enter a reward state
                if maze.get_cell(self.location[0] - 1, self.location[1]).is_entry and maze.agent.get_status() == Status.SEARCHING:
                    self.update_fitness(self.goal_complete_reward)
                    self.set_status(Status.FOUND)
                return

        # If tile is a wall it does not update the agents location and decreases out agents fitness by one
        self.update_fitness(-1)


class Maze:
    map_tiles = {}
    map_graphics = {}
    win = GraphWin("Maze", 500, 500)
    win.setCoords(0, 0, 10, 10)
    agent = Agent()

    def __init__(self, maze_file):
        self.generate_maze(maze_file)

    # Only called during initial map loading
    def decide_cell_type(self, cell_type):
        if cell_type == " ":
            return "Free"
        elif cell_type == "W":
            return "Wall"
        elif cell_type == "E":
            return "Entry"
        elif cell_type == "A":
            return "Agent"
        else:
            raise Exception("Error, incorrect type detected in map file.")

    def decide_agent_starting_location(self):
        Exception("Unimplemented")

        #        rectangle = Rectangle(Point(x, 1), Point(x + 1, 2))
        #        rectangle.setFill("#000000")
        #        rectangle.draw(window)

    def prep_maze_graphics(self, x_pos, y_pos, color, cell_type):
        if cell_type == "Free":
            maze_cell = Rectangle(Point(x_pos + 1, y_pos + 1), Point(x_pos + 2, y_pos + 2))
            maze_cell.setFill(color)
            maze_cell.draw(self.win)

        elif cell_type == "Wall":
            maze_cell = Rectangle(Point(x_pos + 1, y_pos + 1), Point(x_pos + 2, y_pos + 2))
            maze_cell.setFill(color)
            maze_cell.draw(self.win)

        elif cell_type == "Entry":
            maze_cell = Rectangle(Point(x_pos + 1.75, y_pos + 1.75), Point(x_pos + 1.25, y_pos + 1.25))
            maze_cell.setFill(color)
            maze_cell.draw(self.win)

        elif cell_type == "Agent":
            maze_cell = Rectangle(Point(x_pos + 1.75, y_pos + 1.75), Point(x_pos + 1.25, y_pos + 1.25))
            maze_cell.setFill(color)
            maze_cell.draw(self.win)

    # Loads our maze from the .tsv file
    def generate_maze(self, maze_file):

        # Loads the passed in file
        tsv_file = open(maze_file)
        read_tsv = csv.reader(tsv_file, delimiter="\t")

        current_row = 0
        current_column = 0
        for row in read_tsv:
            for x in row:
                # Decides on the Cell type
                if self.decide_cell_type(x) == "Free":
                    new_cell = Free(current_column, current_row)
                    self.map_tiles[(current_column, current_row)] = new_cell

                    self.prep_maze_graphics(current_column, current_row, "#A0A0A0", "Free")

                if self.decide_cell_type(x) == "Wall":
                    new_cell = Wall(current_column, current_row)
                    self.map_tiles[(current_column, current_row)] = new_cell

                    self.prep_maze_graphics(current_column, current_row, "#000000", "Wall")


                if self.decide_cell_type(x) == "Entry":
                    new_cell = Entry(current_column, current_row)
                    self.map_tiles[(current_column, current_row)] = new_cell

                    self.prep_maze_graphics(current_column, current_row, "#00CC00", "Entry")


                if self.decide_cell_type(x) == "Agent":
                    new_cell = Free(current_column, current_row)
                    new_cell.set_contains_agent(True)
                    self.map_tiles[(current_column, current_row)] = new_cell
                    self.agent.set_location(current_column, current_row)

                    self.prep_maze_graphics(current_column, current_row, "#FF0000", "Agent")


                current_column = current_column + 1

            current_row = current_row + 1
            current_column = 0

    # Gets out entry coordinate. Assumes only one exists. None if no entry detected.
    def get_entry_location(self):
        for x in self.map_tiles:
            if self.map_tiles.get(x).is_entry:
                return x

    # Returns the raw data for the cell requested
    def get_cell(self, x_pos, y_pos):
        try:
            return self.map_tiles[(x_pos, y_pos)]
        except:
            Exception("Error, (x_pos, y_pos) does not correspond to a valid map Cell")

    # Returns a string containing the cell type for the cell requested
    def get_cell_type(self, x_pos, y_pos):
        try:
            return self.map_tiles[(x_pos, y_pos)].get_cell_type()
        except:
            Exception("Error, (x_pos, y_pos) does not correspond to a valid map Cell")

    def get_cell_obstruction_cost(self, x_pos, y_pos):
        try:
            return self.map_tiles[(x_pos, y_pos)].obstruction_cost
        except:
            Exception("Error, (x_pos, y_pos) does not correspond to a valid map Cell")


class Cell:
    location = ()
    is_entry = False
    is_free = False
    is_wall = False
    contains_agent = False

    obstruction_cost = 0

    def __init__(self, x_pos, y_pos):
        self.set_location(x_pos, y_pos)

    def get_location(self):
        print(self.location)

    def get_cell_type(self):
        if self.is_free:
            return "Free"
        if self.is_wall:
            return "Wall"
        if self.is_entry:
            return "Entry"

    def get_obstruction_cost(self):
        return self.obstruction_cost

    def get_contains_agent(self):
        return self.contains_agent

    def set_location(self, x_pos, y_pos):
        self.location = (x_pos, y_pos)

    def set_obstruction_cost(self, obstruction_cost):
        self.obstruction_cost = obstruction_cost

    def set_contains_agent(self, contains_agent):
        self.contains_agent = contains_agent

# Currently all Cells default to a pre-set obstruction_cost

class Free(Cell):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)

        self.is_free = True
        self.obstruction_cost = 1


class Entry(Cell):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)

        self.is_entry = True
        self.obstruction_cost = 5


class Wall(Cell):
    def __init__(self, x_pos, y):
        super().__init__(x_pos, y)

        self.is_wall = True
        self.obstruction_cost = 25




maze = Maze("../res/map1.tsv")

# print(maze.map_tiles)
#print(maze.agent.move(Direction.EAST))
print(maze.map_tiles)






#def drawBoard(window, maze_x_length, maze_y_length):
#    for x in range(10):
##        rectangle = Rectangle(Point(x, 1), Point(x + 1, 2))
#        rectangle.setFill("#000000")
#        rectangle.draw(window)


    #window.setBackground("grey")
    #rectangle1 = Rectangle(Point(1, 1), Point(2, 2))
    #rectangle1.setFill("#000000")
    #rectangle1.draw(window)

    #rectangle2 = Rectangle(Point(2, 1), Point(3, 2))
    #rectangle2.setFill("#000000")
    #rectangle2.draw(window)

# (win is window)

#drawBoard(win, 1, 2)
maze.win.setBackground("gray")
maze.win.getMouse()
maze.win.close()

