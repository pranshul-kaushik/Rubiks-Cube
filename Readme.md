```
pip install rubik-solver
```

**Face 1** :- Yellow
**Face 2** :- Blue
**Face 3** :- Red
**Face 4** :- Green
**Face 5** :- Orange
**Face 6** :- White

```python
>>> cube = 'wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby'
>>> from rubik_solver import utils
```
```python
>>> utils.solve(cube, 'Beginner')
```

[F', R, U', R', U, U, F2, Y, B', U, B, U, F2, Y, R', F', U, F, R, U, U, U, F2, Y, L, F, U', F', L', U, F2, Y, L', U, L, U', R, U, R', Y, U', F', U', F, Y, B, U, B', R, U, R', Y, Y, U', L', U, L, U, F, U', F', Y, Y, U2, Y2, U, R, U', R', U', F', U, F, Y, Y, U, R, U', R', U', F', U, F, Y, F, R, U, R', U', F', U2, F, R, U, R', U', F', F, R, U, R', U', F', U, U, U, U, R, U', L', U, R', U', L, R', D', R, D, R', D', R, D, U, R', D', R, D, R', D', R, D, U, U, R', D', R, D, R', D', R, D, U]
```python
>>> utils.solve(cube, 'CFOP')
```
[F', R, U', R', U, U, F2, Y, B', U, B, U, F2, Y, R', F', U, F, R, U, U, U, F2, Y, L, F, U', F', L', U, F2, Y, L', U, L, U', U, F', U, F, U, F', U2, F, Y, U, Y', R', U', R, U2, R', U', R, U, R', U', R, Y, Y, B, U, B', U, F', U2, F, U, F', U2, F, Y, U2, U', R, U, R', U, R, U, R', Y, Y, R', F, R, U, R', F', R, Y, L, U', L', U, Y, Y, Y, Y, U, Y, Y, Y, Y, U, Y, Y, R, U', R, U, R, U, R, U', R', U', R2]
```python
>>> utils.solve(cube, 'Kociemba')
```
[L', F, B2, R', B, R', L, B, D', F', U, B2, U, F2, D', R2, L2, U, F2, D']



[Notation Notes](https://rubiks.fandom.com/wiki/Notation)
