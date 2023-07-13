import pygame
import random
from constants import *
from button import Button, Text
from grid import make_grid, draw, draw_grid, get_clicked_pos
from maze import generate_maze_prim
from algorithms import astar, bfs, dfs, gbfs, dijkstra


# Create a pygame display
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# Get the width and height of the display
win_width, win_height = WIN.get_size()
reset_button = Button(RED, YELLOW, win_width // 2 - 100,
                      (win_height // 2 + 240) - (win_height - 200), 200, 60, text='RESET')
main_menu_button = Button(BLUE, YELLOW, win_width // 2 - 100,
                          (win_height // 2 + 310) - (win_height - 200), 200, 60, text='MAIN')


def run_search(algorithm, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    def reset_maze():
        nonlocal grid, start, end
        grid = make_grid(ROWS, width)
        generate_maze_prim(grid, (ROWS//2, ROWS//2))
        start = None
        end = None
        draw(WIN, grid, ROWS, width)  # Redraw the maze
        pygame.display.update()  # Update the display

    while True:  # Outer loop
        reset_maze()
        start = None
        end = None
        success = False

        # Maze and point selection loop
        while not start or not end:
            draw(WIN, grid, ROWS, width)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()
                elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if start and end:
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)
                success = algorithm(lambda: draw(
                    WIN, grid, ROWS, width), grid, start, end)
                if success:
                    break  # Break the inner loop if algorithm finished successfully

        if success:  # If the search is successful, display the 'RESET' and 'MAIN' buttons
            reset_button = Button(RED, YELLOW, win_width // 2 - 100,
                                  (win_height // 2 + 240) - (win_height - 200), 200, 60, text='RESET')
            main_menu_button = Button(BLUE, YELLOW, win_width // 2 - 100,
                                      (win_height // 2 + 310) - (win_height - 200), 200, 60, text='MAIN')
            while success:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if pygame.mouse.get_pressed()[0]:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        pos_adjusted = (pos[0], pos[1] - (win_height - 200))
                        if reset_button.is_over(pos_adjusted):
                            print("Reset button clicked")
                            break  # Break this loop to restart the outer loop
                        elif main_menu_button.is_over(pos_adjusted):
                            print("Main Menu button clicked")
                            return  # Return to main menu

                # Create a surface for the buttons
                # Note the pygame.SRCALPHA flag
                button_surface = pygame.Surface(
                    (win_width, 200), pygame.SRCALPHA)
                # Fill it with a transparent color
                button_surface.fill((255, 255, 255, 0))

                # Draw the buttons on the button surface
                reset_button.draw(button_surface)
                main_menu_button.draw(button_surface)

                # Blit the button surface onto the main window
                WIN.blit(button_surface, (0, win_height - 200))
                pygame.display.update()


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

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

    instructions = Text('Choose an algorithm, then press Start',
                        win_width // 2 - 75, win_height // 2 - 250)

    selected_algorithm = None  # Variable to store the selected algorithm
    selected_button = None  # Variable to store the selected button
    algorithm_finished = False  # Variable to store whether the algorithm has finished

    running = True
    while running:
        win.fill(WHITE)
        for button in buttons.values():
            button.draw(win)
        start_button.draw(win)
        instructions.draw(win)
        if algorithm_finished:
            reset_button.draw(win)
            main_menu_button.draw(win)
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                if start_button.is_over(pos) and selected_algorithm is not None and not algorithm_finished:
                    print("Start button clicked")
                    algorithm_finished = run_search(selected_algorithm, width)
                elif reset_button.is_over(pos) and algorithm_finished:
                    print("Reset button clicked")
                    run_search(selected_algorithm, width)
                    algorithm_finished = False  # Reset the status
                elif main_menu_button.is_over(pos) and algorithm_finished:
                    print("Main Menu button clicked")
                    running = False  # Stop the current loop
                else:
                    # Check which algorithm button was clicked
                    if buttons['bfs'].is_over(pos):
                        print("BFS selected")
                        selected_algorithm = bfs
                        selected_button = 'bfs'
                    elif buttons['dfs'].is_over(pos):
                        print("DFS selected")
                        selected_algorithm = dfs
                        selected_button = 'dfs'
                    elif buttons['gbfs'].is_over(pos):
                        print("Greedy-BFS selected")
                        selected_algorithm = gbfs
                        selected_button = 'gbfs'
                    elif buttons['astar'].is_over(pos):
                        print("A* selected")
                        selected_algorithm = astar
                        selected_button = 'astar'
                    elif buttons['dijkstra'].is_over(pos):
                        print("Dijkstra selected")
                        selected_algorithm = dijkstra
                        selected_button = 'dijkstra'

                    # Reset all buttons to not selected
                    for button in buttons.values():
                        button.selected = False

                    # Set the clicked button to selected
                    if selected_button:
                        buttons[selected_button].selected = True

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    pygame.font.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finding Algorithm")
    win_width, win_height = pygame.display.get_surface().get_size()

    main(WIN, WIDTH)
