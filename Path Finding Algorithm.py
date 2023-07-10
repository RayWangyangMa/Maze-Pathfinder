import pygame
from queue import PriorityQueue
import random
from A_Star import astar
from BFS import bfs
from DFS import dfs
from GBFS import gbfs
pygame.font.init()

# Setting up the display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node class


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.came_from = None

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def generate_maze(grid, density=0.3):
    for row in grid:
        for node in row:
            if random.random() < density:
                node.make_barrier()


def run_search(algorithm, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    generate_maze(grid, density=0.3)
    start = random.choice(random.choice(grid))
    end = random.choice(random.choice(grid))
    while start == end or start.is_barrier() or end.is_barrier():
        start = random.choice(random.choice(grid))
        end = random.choice(random.choice(grid))

    start.make_start()
    end.make_end()

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    success = algorithm(lambda: draw(WIN, grid, ROWS, width), grid, start, end)

    if success:
        reset_button = Button(RED, 650, 680, 150, 50, text='RESET')
        main_menu_button = Button(BLUE, 650, 740, 150, 50, text='MAIN')

        while True:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.is_over(pos):
                        print('RESET clicked')
                        # Here, instead of returning to the main, we can call run_search again with the same algorithm
                        run_search(algorithm, width)

                    if main_menu_button.is_over(pos):
                        print('Main Menu clicked')
                        # This would take the user back to the main function
                        main(WIN, width)

            # Draw buttons
            reset_button.draw(WIN, BLACK)
            main_menu_button.draw(WIN, BLACK)
            pygame.display.update()


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2,
                                            self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def main(win, width):
    # Create buttons
    bfs_button = Button(GREEN, 10, 10, 150, 50, text='BFS')
    dfs_button = Button(GREEN, 10, 70, 150, 50, text='DFS')
    gbfs_button = Button(GREEN, 10, 130, 150, 50, text='Greedy-BFS')
    astar_button = Button(GREEN, 10, 190, 150, 50, text='A*')

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                if bfs_button.is_over(pos):
                    print('BFS selected')
                    run_search(bfs, width)
                elif dfs_button.is_over(pos):
                    print('DFS selected')
                    run_search(dfs, width)
                elif dfs_button.is_over(pos):
                    print('DFS selected')
                    run_search(dfs, width)
                elif gbfs_button.is_over(pos):
                    print('Greedy-BFS selected')
                    run_search(gbfs, width)
                elif astar_button.is_over(pos):
                    print('A* selected')
                    run_search(astar, width)

        # Redraw the window
        win.fill(WHITE)
        bfs_button.draw(win, BLACK)
        dfs_button.draw(win, BLACK)
        gbfs_button.draw(win, BLACK)
        astar_button.draw(win, BLACK)

        pygame.display.update()

    pygame.quit()


main(WIN, WIDTH)
