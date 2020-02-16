# Board

## Get color of robot and human

```json
{
  "human": 1,
  "robot": 2
}
```

## Transfere board

Every pice has the followint attributes:

+ position (1-32)
+ player (1 or 2)
+ king (True of False)

```python
class Pice
    position: int = 8
    player: int = 1
    king: bool = False

pice_list: List[Pice] = [Piece1, Piece2, ...]

```

## Moving pieces

The roboter gets a List of moves which he has to execute.

```python
class Move:
    origin: int = 8
    target: int = 11

move_list: List[Move] = [Move1, Move2, ...]

return_code = make_move(move_list)

if return_code:
    do_other_stuff_after_move()
```

### Game state

Call the function `update_game_state` of the roboter after every move that has been made.

```python
def update_game_state(player: int, *game_end: bool, *winner: int):
    """
    Update the state of the game
    :param player Whoes turn is it
    :param game_end Has someone won the game
    :param winner Either player1 (1) or player2 (2)
    """
    # ... do something with this information
    pass

```
