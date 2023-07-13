    end = random.choice(random.choice(grid))
    while end == start or end.is_barrier():
        end = random.choice(random.choice(grid))