import pygame

# this class will allow each cell to have its own properties that can be modified
class Cell:
    
    # this is just the initialization function
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.neighbors = []
        self.previous_node = None
        self.wall = False
        self.f_score = float(0)
        self.g_score = float(0)
        self.h_score = float(0)

    # this function adds all the neighbors for each cell
    def addNeighbors(self, grid, column, row, count_diagonal):
        if self.x_pos > 0:
            self.neighbors.append(grid[self.x_pos - 1][self.y_pos])
        if self.x_pos < column - 1:
            self.neighbors.append(grid[self.x_pos + 1][self.y_pos])
        if self.y_pos > 0:
            self.neighbors.append(grid[self.x_pos][self.y_pos - 1])
        if self.y_pos < row - 1:
            self.neighbors.append(grid[self.x_pos][self.y_pos + 1])       
        
        # this extra feature will add all the diagonals as neighbors
        if count_diagonal == True:
            if self.x_pos > 0 and self.y_pos < row - 1:
                self.neighbors.append(grid[self.x_pos - 1][self.y_pos + 1])
            if self.x_pos > 0 and self.y_pos > 0:
                self.neighbors.append(grid[self.x_pos - 1][self.y_pos - 1])
            if self.x_pos < column - 1 and self.y_pos < row - 1:
                self.neighbors.append(grid[self.x_pos + 1][self.y_pos + 1])
            if self.x_pos < column - 1 and self.y_pos > 0:
                self.neighbors.append(grid[self.x_pos + 1][self.y_pos - 1])

    # this function will set the color of the cell
    def colorCell(self, win, color, shape):
        side = 20
        if shape == "node":
            pygame.draw.circle(win, color, (self.x_pos*side+9, self.y_pos*side+9), side//3)
        elif shape == "small square":
            pygame.draw.rect(win, color, (self.x_pos * side, self.y_pos * side, side - 2, side - 2))
        elif shape == "circle":
            pygame.draw.circle(win, color, (self.x_pos*side+9, self.y_pos*side+9), side//6)

