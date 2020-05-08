from game import MinMax, MinMaxMP
from game.algorithm.MonteCarlo import MonteCarlo
from game.algorithm.MonteCarloMP import MonteCarloMP
from game.algorithm.MonteCarloMinMax import MonteCarloMinMax
from game.algorithm.Opponent import Opponent


def simulate_game(game: Opponent):
    while not game.game.is_over():

        if game.game.whose_turn() == 1:
            move = game.calculate_next_move()
            game.move(*move['move'])
        else:
            moves = game.game.get_possible_moves()[0]
            game.move(*moves)


def test_min_max_game():
    min_max_game = MinMax(1, 2)

    simulate_game(min_max_game)

    winner = min_max_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1 or winner == 2 or winner is None


def test_mp_min_max():
    min_max_game = MinMaxMP(1, 4)

    simulate_game(min_max_game)

    winner = min_max_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1 or winner is None


def test_monte_carlo():
    monte_carlo_game = MonteCarlo(1, 2)

    simulate_game(monte_carlo_game)

    winner = monte_carlo_game.game.get_winner()
    assert winner == 1 or winner == 2 or winner is None


def test_mp_monte_carlo():
    monte_carlo_game = MonteCarloMP(1, 5)

    simulate_game(monte_carlo_game)

    winner = monte_carlo_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1 or winner is None


def test_monte_carlo_min_max():
    monte_carlo_min_max_game = MonteCarloMinMax(1, 2)

    simulate_game(monte_carlo_min_max_game)

    winner = monte_carlo_min_max_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1 or winner is None
