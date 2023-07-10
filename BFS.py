import pygame
from queue import Queue

# Breath-First Search (BFS) algorithm


def bfs(draw, grid, start, end):
    visited = set()
    queue = Queue()
    queue.put(start)
    visited.add(start)

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

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
                queue.put(neighbor)
                visited.add(neighbor)
                neighbor.came_from = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

        pygame.event.pump()  # Process event queue
        pygame.display.update()  # Update the display

    return False
