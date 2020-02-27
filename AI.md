# Neuronal Network

## 

### Input

Input is the current game 

+ 32 long 1 dim Array
+ (0, 0, 0) = None
+ Player 1: 
    + (1, 0, 0) = Normal Piece
    + (1, 1, 0) = King
+ Player 2:
    + (0, 0, 1) = Normal Piece
    + (0, 1, 1) = King

### Output

+ Pick two numbers from the range 1 - 32


## Learning

### Steps

1. Play against the random algorithm to learn valid moves
2. Play against itself (or other generation)


1. Punish if not a valid move = Lost game
2. Punish if KI looses the game
    + Lost = -1
    + Draw = 0
    + Win = 1

