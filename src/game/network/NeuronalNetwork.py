import torch
import torch.nn as nn
import torch.nn.functional as F

from game.network.Game import NCheckersGame


class Checkers(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(32 * 3, 48)
        self.fc2 = nn.Linear(48, 24)
        self.fc3 = nn.Linear(24, 6)
        self.fc4 = nn.Linear(6, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return F.log_softmax(x, dim=1)


game = NCheckersGame()
flatten_board = game.board_to_flat_matrix()

input_board = torch.tensor(flatten_board, dtype=torch.float).view(-1, 96)

checker = Checkers()
move = checker(input_board).tolist()
start = move[0][0]
end = move[0][1]
print(start, end)

try:
    game.move([start, end])
except ValueError:
    pass
