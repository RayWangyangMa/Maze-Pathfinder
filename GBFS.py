import pygame
from queue import PriorityQueue


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


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
