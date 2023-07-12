import pygame
from collections import deque
from queue import PriorityQueue, Queue


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            temp = current
            while temp in came_from:
                temp = came_from[temp]
                temp.make_path()
                draw()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


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


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
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
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def gbfs(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    h_score = {node: float("inf") for row in grid for node in row}
    h_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            temp = current
            while temp in came_from:
                temp = came_from[temp]
                temp.make_path()
                draw()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_h_score = h(neighbor.get_pos(), end.get_pos())

            if temp_h_score < h_score[neighbor]:
                came_from[neighbor] = current
                h_score[neighbor] = temp_h_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((h_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


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
