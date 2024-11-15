import pygame
import sys
from random import randrange
#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
#width and height of grids
WIDTH = 30
HEIGHT = 30
#number of squares
NUMSQUARES = 10
MARGIN = 2.5
MENU_SIZE = 50
LEFT_CLICK = 1
RIGHT_CLICK = 3

class Minesweeper:
    def __init__(self):
        screen.fill(BLACK)
        #draw grid
        for row in range(self.squaresnum_y):
            for column in range(self.squaresnum_x):
                color = WHITE
                if self.grid[row][column].is_visible:
                    color = RED if self.grid[row][column].has_bomb else GRAY
                elif self.grid[row][column].has_flag:
                    color = BLUE
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN + MENU_SIZE,
                                      WIDTH,
                                      HEIGHT])
                    self.grid[row][column].show_text()
    def game_over(self):
        for row in range(self.squaresnum_y):
            for column in range(self.squaresnum_x):
                if self.grid[row][column].has_bomb:
                    self.grid[row][column].is_visible = True
                self.grid[row][column].has_flag = False
    def change_num_bombs(self, bombs):
        self.num_bombs += bombs
        if self.num_bombs < 1:
            self.num_bombs = 1
        elif self.num_bombs > (self.squaresnum_x * self.squaresnum_y) // 3:
            self.num_bombs = (self.squaresnum_x * self.squaresnum_y) //3
        self.reset_game()
    def place_bombs(self, row, column):
        bombplaced = 0
        while bombplaced < self.num_bombs:
            x = randrange(self.squaresnum_y)
            y = randrange(self.squaresnum_x)
            if not self.grid[x][y].has_bomb and not (row == x and column == y):
                self.grid[x][y].has_bomb = True
                bombplaced += 1
        self.count_all_bombs()
        if self.grid[row][column].bomb_count != 0:
            self.reset_game()
            self.place_bombs(row, column)
    def count_all_bombs(self):
        for row in range (self.squaresnum_y):
            for column in range(self.squaresnum_x):
                self.grid[row][column].count_bombs(self.squaresnum_y, self.squaresnum_x)
    def reset_game(self):
        for row in range(self.squaresnum_y):
            for column in range(self.squaresnum_x):
                self.init = False
                self.grid[row][column].is_visible = False
                self.grid[row][column].has_bomb = False
                self.grid[row][column].bomb_count = 0
                self.grid[row][column].test = False
                self.grid[row][column].has_flag = False
                self.game_lost = False
                self.game_won = False
                self.flag_count = 0
    def check_victory(self):
        count = 0
        total = self.squaresnum_x * self.squaresnum_y
        for row in range(self.squaresnum_y):
            for column in range(self.squaresnum_x):
                if self.grid[row][column].is_visible:
                    count += 1
        if ((total - count) == self.num_bombs) and not self.game_lost:
            self.game_won = True
            for row in range(self.squaresnum_y):
                for column in range(self.squaresnum_x):
                    if self.grid[row][column].has_bomb:
                            self.grid[row][column].has_flag = True
    def count_flags(self):
        total_flags = 0
        for row in range(squaresnum_y):
            for column in range(squaresnum_x):
                if self.grid[row][column].has_flag:
                    total_flags += 1
        self.flag_count = total_flags
    def click_handle(self, row, column, button):
        if button == LEFT_CLICK and self.game_won:
            self.reset_game()
        elif button = RIGHT_CLICK and not self.grid[row][column].has_flag:
            if not self.game_lost:
                if not self.init:
                    self.place_bombs(row, column)
                    self.init = True
                self.grid[row][column].is_visible = True
                self.grid[row][column].has_flag = True
                if self.grid[row][column].has_bomb:
                    self.game_over()
                    self.game_lost = True
                if self.grid[row][column].bomb_count == 0 and not self.grid[row][column].has_bomb:
                    self.grid[row][column].open_neighbors(self.squaresnum_y, squaresnum_x)
                self.check_victory()
            else:
                self.game_lost = False
                self.reset_game()
        elif button == RIGHT_CLICK and not self.game_won:
            if not self.grid[row][column].has_flag:
                if self.flag_count < self.num_bombs and not self.grid[row][column].is_visible:
                    self.grid[row][column].has_flag = True
            else:
                self.grid[row][column].has_flag = False
            self.count_flags()
