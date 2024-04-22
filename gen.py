import random
import sys
from math import sqrt

N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
def print_grid(grid, mask=False):
    print('-' * N)
    for row in grid:
        print(''.join(row))
    print('-' * N)

def print_playable_grid(grid, rows, cols):
    row_padding = max(len(str(i)) for i in rows) + 1
    col_padding = max(len(str(i)) for i in cols) + 1
    row_str = [str(i).rjust(row_padding) for i in rows]
    col_str = [str(i).rjust(col_padding) for i in cols]
    
    grid_out = [[' ' for i in range(N + 2 + row_padding)] for j in range(N + 2 + col_padding)]

    for i in range(N):
        for j in range(row_padding):
            grid_out[i + col_padding + 1][j] = row_str[i][j]
    
    for i in range(col_padding):
        for j in range(N):
            grid_out[i][j + row_padding + 1] = col_str[j][i]

    grid_out[col_padding][row_padding] = '┌'
    grid_out[col_padding][N + row_padding + 1] = '┐'
    grid_out[N + col_padding + 1][row_padding] = '└'
    grid_out[N + col_padding + 1][N + row_padding + 1] = '┘'
    
    for i in range(N):
        grid_out[col_padding + 1 + i][row_padding] = '│'
        grid_out[col_padding + 1 + i][N + row_padding + 1] = '│'
        grid_out[col_padding][row_padding + 1 + i] = '─'
        grid_out[N + col_padding + 1][row_padding + 1 + i] = '─'

    for i in range(N):
        for j in range(N):
            if grid[i][j] in '12|-':
                grid_out[col_padding + 1 + i][row_padding + 1 + j] = ' '
            else:
                grid_out[col_padding + 1 + i][row_padding + 1 + j] = grid[i][j]

    for row in grid_out:
        print(''.join(row))

total = (N * N) // 2
def generate_grid(grid, total):
    missing = random.randint(int(sqrt(max(0, N // 2 - 5))), 2 * N // 3)

    for i in range(total - missing):
        seen = set()
        x, y = random.randint(0, N - 1), random.randint(0, N - 1)
        while True:
            x, y = random.randint(0, N - 1), random.randint(0, N - 1)
            typ = random.randint(0, 1)

            if typ == 0 and x > 0 and grid[x - 1][y] == ' ' and grid[x][y] == ' ':
                grid[x][y] = '|'
                grid[x - 1][y] = '1'
                break
            
            elif typ == 1 and y < N - 1 and grid[x][y + 1] == ' ' and grid[x][y] == ' ':
                grid[x][y] = '-'
                grid[x][y + 1] = '2'
                break

            seen.add((x, y, typ))
            if len(seen) == N * N * 2:
                print('Failed to generate grid', i, f'{i / (total - missing) * 100:.4f}')
                if i > (total - missing) * 0.94: # 94% filled, pass
                    print("Passed Check 1")
                    return grid, (total - i)
                
                if N > 30 and i > (total - missing) * 0.91: # 91% filled, pass
                    print("Passed Check 2")
                    return grid, (total - i)

                return None, None
    
    return grid, missing

while True:
    empty_grid = [[' ' for i in range(N)] for j in range(N)]
    grid, blockers = generate_grid(empty_grid.copy(), total)
    if grid: break

blockers = 2 * blockers + N % 2
for i in range(N):
    for j in range(N):
        if grid[i][j] == ' ':
            grid[i][j] = 'X'    

print(f'{N} x {N} grid with {blockers} blockers')
print_grid(grid)

rows = []
cols = []
for i in range(N):
    rows.append(sum(int(c) for c in grid[i] if c in '12'))
    cols.append(sum(int(grid[j][i]) for j in range(N) if grid[j][i] in '12'))

print(f'{rows = }')
print(f'{cols = }')
print_playable_grid(grid, rows, cols)

