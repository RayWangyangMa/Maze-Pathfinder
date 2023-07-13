import pygame
import random
from constants import *
from button import Button, Text
from grid import make_grid, draw, draw_grid, get_clicked_pos
from maze import generate_maze_prim
from algorithms import astar, bfs, dfs, gbfs, dijkstra


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


def main(win, width):
    # Create buttons with normal and selected colors
    buttons = {
        'bfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 180, 200, 60, text='BFS'),
        'dfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 110, 200, 60, text='DFS'),
        'gbfs': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 - 40, 200, 60, text='Greedy-BFS'),
        'astar': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 + 30, 200, 60, text='A*'),
        'dijkstra': Button(GREEN, YELLOW, win_width // 2 - 100, win_height // 2 + 100, 200, 60, text='Dijkstra'),
    }
    start_button = Button(ORANGE, YELLOW, win_width // 2 -
                          100, win_height // 2 + 170, 200, 60, text='Start')

    font = pygame.font.SysFont('arial', 30)
    text_surface = font.render(
        'Choose an algorithm, then press Start', True, BLACK)
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


if __name__ == "__main__":
    pygame.font.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finding Algorithm")
    win_width, win_height = pygame.display.get_surface().get_size()

    main(WIN, WIDTH)
