import pygame
from collections import deque

# Depth-First Search (DFS) algorithm


def dfs(draw, grid, start, end):
    visited = set()
    stack = deque()
    stack.append(start)
    visited.add(start)

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            temp = current
            while temp is not None:
                temp.make_path()
                temp = temp.came_from
                draw()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                neighbor.came_from = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

        pygame.event.pump()  # Process event queue
        pygame.display.update()  # Update the display

    return False
