def main(win, width):
    # Create buttons
    bfs_button = Button(GREEN, 10, 70, 150, 50, text='BFS')
    dfs_button = Button(GREEN, 10, 130, 150, 50, text='DFS')
    gbfs_button = Button(GREEN, 10, 190, 150, 50, text='Greedy-BFS')
    astar_button = Button(GREEN, 10, 10, 150, 50, text='A*')

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