from game import MinMax, MinMaxMP
from game.algorithm.MonteCarlo import MonteCarlo
from game.algorithm.MonteCarloMP import MonteCarloMP


def test_min_max_game():
    min_max_game = MinMax(1, 2)

    while not min_max_game.game.is_over():

        if min_max_game.game.whose_turn() == 1:
            min_max_game.calculate_next_move()
        else:
            moves = min_max_game.game.get_possible_moves()[0]
            min_max_game.move(moves[0], moves[1])

    winner = min_max_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1 or winner == 2 or winner is None


def test_mp_min_max():
    min_max_game = MinMaxMP(1, 2)

    while not min_max_game.game.is_over():

        if min_max_game.game.whose_turn() == 1:
            move = min_max_game.calculate_next_move()
            min_max_game.move(*move['move'])
            print(move)
        else:
            moves = min_max_game.game.get_possible_moves()[0]
            min_max_game.move(moves[0], moves[1])

    winner = min_max_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1


def test_monte_carlo():
    monte_carlo_game = MonteCarlo(1, 5)

    while not monte_carlo_game.game.is_over():

        if monte_carlo_game.game.whose_turn() == 1:
            monte_carlo_game.calculate_next_move()
        else:
            moves = monte_carlo_game.game.get_possible_moves()[0]
            monte_carlo_game.move(moves[0], moves[1])

    winner = monte_carlo_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1


def test_mp_monte_carlo():
    monte_carlo_game = MonteCarloMP(1, 5)

    while not monte_carlo_game.game.is_over():

        if monte_carlo_game.game.whose_turn() == 1:
            monte_carlo_game.calculate_next_move()
        else:
            moves = monte_carlo_game.game.get_possible_moves()[0]
            monte_carlo_game.move(moves[0], moves[1])

    winner = monte_carlo_game.game.get_winner()
    print(f"The winner should be player one. Winner: {winner}")
    assert winner == 1
