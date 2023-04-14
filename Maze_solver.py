# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:08:16 2022

@author: AhmedZ
"""

import pygame
import math
import random
from queue import PriorityQueue
import numpy as np

pygame.init()

class DrawInfo:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (125, 125, 125)
    
    GREEN = (0, 255, 0)
    RED = (255,99,71)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    TURQUOISE = (64, 224, 208)
    
    START_COLOR = ORANGE
    END_COLOR = TURQUOISE
    
    BLOCK_WIDTH = 15
    PAD = 1
    
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    

    
    
class Spot:
    
    def __init__(self,draw_info, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col *width
        
        self.width = width
        self.total_rows = total_rows
        self.draw_info = draw_info
        self.color = self.draw_info.WHITE
    
    def get_pos(self):
        return self.row, self.col
     
# Check color
    def is_closed(self):
        return self.color == self.draw_info.RED
    
    def is_open(self):
        return self.color == self.draw_info.GREEN
    
    def is_barrier(self):
        return self.color == self.draw_info.BLACK
    
    def is_start(self):
        return self.color ==self.draw_info.START_COLOR
    
    def is_end(self):
        return self.color == self.draw_info.END_COLOR
    
    def reset(self):
        self.color = self.draw_info.WHITE

# Change color
    def make_closed(self):
        self.color = self.draw_info.RED
    
    def make_open(self):
        self.color = self.draw_info.GREEN
    
    def make_barrier(self):
        self.color = self.draw_info.BLACK
    
    def make_start(self):
        self.color  = self.draw_info.START_COLOR
    
    def make_end(self):
        self.color = self.draw_info.END_COLOR
    
    def make_path(self):
        self.color = self.draw_info.PURPLE
    
    def draw(self, window):
        pygame.draw.rect(window, self.color,(self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        
        # UP
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        
        # Down
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        
        # Right
        if self.col < self.total_rows -1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        
        # Left
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
            
        
        # # UP Right
        # if self.row > 0 and self.col < self.total_rows -1 and not grid[self.row-1][self.col+1].is_barrier():
        #     self.neighbors.append(grid[self.row-1][self.col+1])
        
        # # UP Left
        # if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_barrier():
        #     self.neighbors.append(grid[self.row-1][self.col-1])
            
        # # Down Right
        # if self.row < self.total_rows -1 and self.col < self.total_rows -1 and not grid[self.row+1][self.col+1].is_barrier():
        #     self.neighbors.append(grid[self.row+1][self.col+1])
        
        # # Down Left
        # if self.row < self.total_rows -1 and self.col > 0 and not grid[self.row+1][self.col-1].is_barrier():
        #     self.neighbors.append(grid[self.row+1][self.col-1])
        
            
        
    
    def __lt__(self, other):
        return False



def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    
    return np.sqrt(abs(x1-x2) + abs(y1-y2))

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        
    
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
    
    return False

        
        
    
    
def make_grid(draw_info,rows, width):
    
    grid = []
    gap = width // rows
 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(draw_info, i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(draw_info, window, rows, width):
    gap = width // rows
    
    for i in range(rows):
        pygame.draw.line(window, draw_info.GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(window, draw_info.GREY,(j*gap,0),(j*gap,width))

def draw(draw_info,window, grid, rows, width):
    window.fill(draw_info.WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(window)
    
    draw_grid(draw_info,window, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col



def main():
    
    draw_info = DrawInfo()
    width = 800
    rows = 50
    window = pygame.display.set_mode((width, width))
    pygame.display.set_caption('A* Algorithm Path Finder')
    grid = make_grid(draw_info,rows, width)
    
    start = None
    end = None
    
    run = True
    
    while run:
        draw(draw_info, window, grid,rows, width)
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
     
         
            if pygame.mouse.get_pressed()[0]:
     
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                spot = grid[row][col]
                if not start and spot !=end:
                    start = spot
                    start.make_start()
                    
         
                elif not end and spot !=start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot !=start:
                    spot.make_barrier()
                    
                    
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                
          
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(draw_info, window, grid, rows, width), grid, start, end)   
                    
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                
            
    
    
    
    pygame.quit()
    
    
    
    
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
            













    
    