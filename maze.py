import random


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
