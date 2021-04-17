import pygame
import math
import sys
from cell import Cell
import PySimpleGUI as gui

# this function exits the pygame window and ends the program
def exitProgram():
    pygame.quit()
    sys.exit()

# this function will determine what cell the mouse if hovering over and then change the state of the cell
def selectWall(mouse_pos, new_state, end_node, start_node):
    x = mouse_pos[0] // 20
    y = mouse_pos[1] // 20
    if grid[x][y] != end_node and grid[x][y] != start_node:
        grid[x][y].wall = new_state

def selectStart(mouse_pos, start_node, end_node):
    x = mouse_pos[0] // 20
    y = mouse_pos[1] // 20
    if grid[x][y] != end_node:
        return grid[x][y]
    else:
        return start_node   

def selectEnd(mouse_pos, start_node , end_node):
    x = mouse_pos[0] // 20
    y = mouse_pos[1] // 20
    if grid[x][y] != start_node:
        return grid[x][y]
    else:
        return end_node

def heuristic(current_node, end_node):
    return math.sqrt((current_node.x_pos - end_node.x_pos)**2 + abs(current_node.y_pos - end_node.y_pos)**2)  

def drawGrid():
    window.fill((127, 195, 180))
    for y in range(grid_rows):
        for x in range(grid_col):
            cell = grid[x][y]
            cell.colorCell(window, (244,250,250), "small square")
            if cell == start:
                cell.colorCell(window, (0, 153, 0), "circle")
            elif cell in path:
                cell.colorCell(window, (24, 110, 110), "small square")
            elif cell in closed_set:
                cell.colorCell(window, (255, 153, 51), "small square")
            elif cell in open_set:
                cell.colorCell(window, (255, 153, 51), "circle")
            elif cell == end:
                cell.colorCell(window, (204, 0, 0), "circle")
            elif cell.wall:
                cell.colorCell(window, (2, 28, 48), "small square")
                
    pygame.display.update()

def aStarBackTrack(current):
    temp_node = current
    while temp_node.previous_node:
        path.append(temp_node.previous_node)
        temp_node = temp_node.previous_node


def aStarSearch():

    start.h_score = heuristic(start, end)
    open_set.append(start)    
    while len(open_set) > 0:
        lowest_f_score_index = 0
        for index in range(len(open_set)):
            if open_set[index].f_score < open_set[lowest_f_score_index].f_score:
                lowest_f_score_index = index

        current_node = open_set[lowest_f_score_index]
        
        
        if current_node == end:
            aStarBackTrack(current_node)
            print("Solution found.")
            return 

        open_set.remove(current_node)
        closed_set.append(current_node)

        for neighbor in current_node.neighbors:
            
            if neighbor in closed_set or neighbor.wall:
                continue
            
            new_g_score = current_node.g_score + 1
            use_new_path = False
            
            if neighbor in open_set:
                if new_g_score < neighbor.g_score:
                    neighbor.g_score = new_g_score
                    use_new_path = True
            
            else:
                neighbor.g_score = new_g_score
                use_new_path = True
                open_set.append(neighbor)
            
            if use_new_path == True:
                neighbor.h_score = heuristic(neighbor, end)
                neighbor.f_score = neighbor.g_score + neighbor.h_score
                neighbor.previous_node = current_node
        
        drawGrid()
    print("No sol.")
    
def displayImage(image):    
    window.blit(image, (0,0))
    pygame.display.flip()

def displayPages():
    tutorial_images = [pygame.image.load('images/screen_1.jpg'), pygame.image.load('images/screen_2.jpg'), pygame.image.load('images/screen_3.png'), pygame.image.load('images/screen_4.jpg'), 
    pygame.image.load('images/screen_5.jpg'), pygame.image.load('images/screen_6.jpg'), pygame.image.load('images/screen_7.jpg')]
    tutorial_index = 0

    while tutorial_index < len(tutorial_images):
        displayImage(tutorial_images[tutorial_index])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitProgram()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tutorial_index += 1
                if event.key == pygame.K_LEFT:
                    if tutorial_index != 0:
                        tutorial_index-= 1
        
# initializes variables; most of these are temporary until the gui is added
grid = []
side_length = 20
white = (0, 60, 60)
grid_rows = 40
grid_col = 60
is_diagonal = True
screen_length = grid_col * side_length
screen_width = grid_rows * side_length
screen_size = (screen_length, screen_width)

# initializes the pygame application
pygame.init() 
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pathfinding Visualizer")
clock = pygame.time.Clock()

displayPages()

while True:

    # adds all the cells to the grid
    for x in range(grid_col):
        lis = []
        for y in range(grid_rows):
            lis.append(Cell(x, y))
        grid.append(lis)

    # adds the neighbors of all the cells in the grid
    for x in range(grid_col):
        for y in range(grid_rows):
            grid[x][y].addNeighbors(grid, grid_col, grid_rows, is_diagonal)
            grid[x][y].wall = False

    start = grid[5][18]
    end = grid[54][18]
    start_search = False
    open_set = []
    closed_set = []
    path = []
    is_selecting_walls = False
    is_selecting_start = True
    is_selecting_end = False
    reset_game = False

    drawGrid()
    pygame.display.flip()

    while True:
        
        if is_selecting_start == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    if event.button in (1, 3): 
                        start = selectStart(pygame.mouse.get_pos(), start, end)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_selecting_start = False
                        is_selecting_end = True
                    if event.key == pygame.K_c:
                        reset_game = True
        
        if is_selecting_end == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    if event.button in (1, 3): 
                        end = selectEnd(pygame.mouse.get_pos(), start, end)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_selecting_end = False
                        is_selecting_walls = True
                    if event.key == pygame.K_c:
                        reset_game = True

        if is_selecting_walls == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    if event.button in (1, 3): 
                        selectWall(pygame.mouse.get_pos(), event.button==1, end, start)
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] or event.buttons[2]:  
                        selectWall(pygame.mouse.get_pos(), event.buttons[0], end, start) 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_search = True
                        is_selecting_wall = False
                    if event.key == pygame.K_c:
                        reset_game = True

        if reset_game == True:
            break

        if start_search == True:
            aStarSearch()
            start_search = False
        
        drawGrid()
        pygame.display.flip()
            

            
    