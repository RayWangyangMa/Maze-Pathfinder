import pygame
from queue import PriorityQueue
import random
from A_Star import astar
from BFS import bfs
from DFS import dfs
from GBFS import gbfs
from Dijkstra import dijkstra
pygame.font.init()

# Setting up the display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")
win_width, win_height = pygame.display.get_surface().get_size()
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

class Text:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw(self, win):
        font = pygame.font.SysFont('arial', 30)
        text_surface = font.render(self.text, True, BLACK)
        win.blit(text_surface, (self.x, self.y))

def generate_maze_prim(grid, start):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    # Initially mark all cells as walls
    for row in grid:
        for node in row:
            node.make_barrier()

    # Start with a grid full of walls
    x, y = start
    grid[x][y].reset()

    wall_list = [(x + dx[i], y + dy[i], i) for i in range(4)]
    while wall_list:
        random.shuffle(wall_list)
        wx, wy, wi = wall_list.pop()

        px, py = wx + dx[wi], wy + dy[wi]

        if px >= 0 and py >= 0 and px < len(grid) and py < len(grid[0]) and grid[px][py].is_barrier():
            grid[wx][wy].reset()
            grid[px][py].reset()

            for i in range(4):
                nx, ny = px + dx[i], py + dy[i]
                if nx >= 0 and ny >= 0 and nx < len(grid) and ny < len(grid[0]) and grid[nx][ny].is_barrier():
                    wall_list.append((nx, ny, i))


def run_search(algorithm, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = random.choice(random.choice(grid))
    while start.is_barrier():
        start = random.choice(random.choice(grid))

    generate_maze_prim(grid, (start.row, start.col))

    end = random.choice(random.choice(grid))
    while end == start or end.is_barrier():
        end = random.choice(random.choice(grid))

    start.make_start()
    end.make_end()

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    success = algorithm(lambda: draw(WIN, grid, ROWS, width), grid, start, end)

    if success:
        reset_button = Button(RED, YELLOW, 650, 680, 150, 50, text='RESET')
        main_menu_button = Button(BLUE, YELLOW, 650, 740, 150, 50, text='MAIN')

        running = True
        while running:
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
                        running = False

                    if main_menu_button.is_over(pos):
                        print('Main Menu clicked')
                        # This would take the user back to the main function
                        main(WIN, width)
                        running = False

            # Draw buttons
            reset_button.draw(WIN, BLACK)
            main_menu_button.draw(WIN, BLACK)
            pygame.display.update()


class Button:
    def __init__(self, color, selected_color, x, y, width, height, text=''):
        self.color = color
        self.selected_color = selected_color  # Add this line
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False  # Add this line

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2,
                                            self.width+4, self.height+4), 0)

        if self.selected:  # Add this if-else block
            pygame.draw.rect(win, self.selected_color, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

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
    # Create buttons with normal and selected colors
    buttons = {
        'bfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 180, 200, 60, text='BFS'),
        'dfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 110, 200, 60, text='DFS'),
        'gbfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 40, 200, 60, text='Greedy-BFS'),
        'astar': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 + 30, 200, 60, text='A*'),
        'dijkstra': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 + 100, 200, 60, text='Dijkstra'),
    }
    start_button = Button(ORANGE, YELLOW, win_width // 2 - 100, win_height // 2 + 170, 200, 60, text='Start')
    
    font = pygame.font.SysFont('arial', 30)
    text_surface = font.render('Choose an algorithm, then press Start', True, BLACK)
    text_width, text_height = text_surface.get_size()

    instructions = Text('Choose an algorithm, then press Start',
                        win_width // 2 - text_width // 2,
                        win_height // 2 - 250)

    selected_algorithm = None  # Variable to store the selected algorithm
    selected_button = None  # Variable to store the selected button

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                if buttons['bfs'].is_over(pos):
                    print('BFS selected')
                    selected_algorithm = bfs
                    selected_button = 'bfs'
                elif buttons['dfs'].is_over(pos):
                    print('DFS selected')
                    selected_algorithm = dfs
                    selected_button = 'dfs'
                elif buttons['gbfs'].is_over(pos):
                    print('Greedy-BFS selected')
                    selected_algorithm = gbfs
                    selected_button = 'gbfs'
                elif buttons['astar'].is_over(pos):
                    print('A* selected')
                    selected_algorithm = astar
                    selected_button = 'astar'
                elif buttons['dijkstra'].is_over(pos):
                    print('Dijkstra selected')
                    selected_algorithm = dijkstra
                    selected_button = 'dijkstra'
                elif start_button.is_over(pos) and selected_algorithm is not None:
                    print('Start button clicked')
                    run_search(selected_algorithm, width)

                # Reset all buttons to not selected
                for button in buttons.values():
                    button.selected = False
                # Set the clicked button to selected
                if selected_button:
                    buttons[selected_button].selected = True

        # Redraw the window
        win.fill(WHITE)
        for button in buttons.values():
            button.draw(win, BLACK)
        start_button.draw(win, BLACK)
        instructions.draw(win)

        pygame.display.update()

    pygame.quit()




main(WIN, WIDTH)
