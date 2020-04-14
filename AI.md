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
*Possibility 1:*

+ Pick two numbers from the range 1 - 32

*Possibility 2:*
```
Vector 1 size(1, 32) -> Piece that should be moved
Vector 2 size(1, 32) -> Piece Position, where it should go.

Output: Vector (1, 64)
```


## Learning

### Steps

1. Play against the random algorithm to learn valid moves
2. Play against itself (or other generation)


1. Punish if not a valid move = Lost game
2. Punish if KI looses the game
    + Lost = -1
    + Draw = 0
    + Win = 1

### Q Learning
![](https://wikimedia.org/api/rest_v1/media/math/render/svg/678cb558a9d59c33ef4810c9618baf34a9577686)
https://en.wikipedia.org/wiki/Q-learning


# Sources
https://www.researchgate.net/publication/242405861_Reinforcement_learning_project_AI_Checkers_Player
https://www.youtube.com/watch?v=qfovbG84EBg
