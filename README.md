# DominoFit Solver

Sat Solver in Z3 for the fun puzzle game [DominoFit](https://dominofit.isotropic.us/). Also includes a generator just because (not very good)

## Requirements

You just need to have the z3 library installed via
```bash
pip install z3-solver
```
Then the solver will work.

`gen.py` works without any installed libraries. 

## Usage

To generate a puzzle, all you need to do is run `gen.py` with the desired dimensions of the puzzle. For example, to generate a 5x5 puzzle, you would run
```bash
python3 gen.py 5
```
```
5 x 5 grid with 7 blockers
-----
-2XX1
XX-2|
-2X1X
1-2|X
|-2-2
-----
rows = [3, 2, 3, 3, 4]
cols = [1, 4, 4, 3, 3]
         
   14433 
  ┌─────┐
 3│  XX │
 2│XX   │
 3│  X X│
 3│    X│
 4│     │
  └─────┘
```
It first outputs a valid solution to the given grid, then the proper playing grid. The default size with no arguments is a 7 x 7 grid.

To run the solver, you need to first input the size of the grid, then the grid itself, and finally the row and column constraints. For example, to solve the above puzzle, you would run
```bash
python3 solver.py
```
```
size? > 5
  XX 
XX   
  X X
    X
     
rows? > [3, 2, 3, 3, 4]
cols? > [1, 4, 4, 3, 3]
```
This outputs the solution to the puzzle:
```
-----
-2XX1
XX-2|
-2X1X
1-2|X
|-2-2
-----
```
2 dominoes are marked with `-` on the empty tile, and 1 dominoes are marked with `|` on empty tile.

## Notes
- `gen.py` can produce puzzles with more than one valid solution if the board is large enough. See the % generation requirements.
- If the puzzle has more than one valid solution, the solver will output all of them in a non-specified order. 
- I didn't really double-check the solver constraints, hopefully they're correct (they've been fine for now but make an issue if needed).