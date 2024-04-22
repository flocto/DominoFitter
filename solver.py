import z3


def print_grid(grid, mask=False):
    print('-' * N)
    for row in grid:
        if mask:
            print(''.join(row).replace('1', ' ').replace(
                '2', ' ').replace('-', ' ').replace('|', ' '))
        else:
            print(''.join(row))
    print('-' * N)


N = int(input('size? > '))

grid = []
for i in range(N):
    grid.append(list(input()))

rows = eval(input('rows? > '))
cols = eval(input('cols? > '))

s = z3.Solver()
eqs = []
grid_symbols = [[z3.Int(f'grid_{i}_{j}') for j in range(N)] for i in range(N)]

# domain
for i in range(N):
    for j in range(N):
        eqs.append(z3.And(grid_symbols[i][j] >= 0, grid_symbols[i][j] <= 2))

# blockers
for i in range(N):
    for j in range(N):
        if grid[i][j] == 'X':
            eqs.append(grid_symbols[i][j] == 0)

            if i > 0:
                eqs.append(grid_symbols[i - 1][j] != 1)
            if j < N - 1:
                eqs.append(grid_symbols[i][j + 1] != 2)

# row/col sum
for i in range(N):
    eqs.append(sum([grid_symbols[i][j] for j in range(N)]) == rows[i])
    eqs.append(sum([grid_symbols[j][i] for j in range(N)]) == cols[i])

# domino constraints
for i in range(N):
    for j in range(N):
        # horizontal and vertical dominoes cannot exist on the wrong edges
        if i == N - 1:
            eqs.append(grid_symbols[i][j] != 1)
        if j == 0:
            eqs.append(grid_symbols[i][j] != 2)

        if i > 0 and grid[i - 1][j] == ' ' and grid[i][j] == ' ':
            # vertical domino
            eqs.append(z3.If(grid_symbols[i - 1][j]
                       == 1, grid_symbols[i][j] == 0, True))

        if j > 0 and grid[i][j - 1] == ' ' and grid[i][j] == ' ':
            # horizontal domino
            eqs.append(z3.If(grid_symbols[i][j] ==
                       2, grid_symbols[i][j - 1] == 0, True))

        # ensures that if there is a cell with 0 value and its not a blocker, it must be part of a valid domino
        up, right = False, False
        if i > 0 and grid[i - 1][j] == ' ' and grid[i][j] == ' ':
            up = grid_symbols[i - 1][j] == 1
        if j < N - 1 and grid[i][j + 1] == ' ' and grid[i][j] == ' ':
            right = grid_symbols[i][j + 1] == 2

        if grid[i][j] == ' ':
            eqs.append(z3.If(grid_symbols[i][j] == 0, z3.Xor(up, right), True))

s.add(eqs)

if s.check() == z3.sat:
    while s.check() == z3.sat:
        m = s.model()
        grid_filled = [[' ' for i in range(N)] for j in range(N)]
        for i in range(N):
            for j in range(N):
                grid_filled[i][j] = str(m[grid_symbols[i][j]])

                if grid[i][j] == 'X':
                    grid_filled[i][j] = 'X'

        for i in range(N):
            for j in range(N):
                if grid_filled[i][j] == '1':
                    grid_filled[i + 1][j] = '|'
                elif grid_filled[i][j] == '2':
                    grid_filled[i][j - 1] = '-'

        print_grid(grid_filled)

        b3_sym = b3 = 0
        for i in range(N):
            for j in range(N):
                b3 *= 3
                b3 += int(m[grid_symbols[i][j]].as_long())

                b3_sym *= 3
                b3_sym += grid_symbols[i][j]

        s.add(b3_sym != b3)
else:
    print('no solution')
