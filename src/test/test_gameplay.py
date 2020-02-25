from difficulty import Random, MinMax


def test_random_game():
    random_game = Random(1)

    while not random_game.game.is_over():

        if random_game.game.whose_turn() == 1:
            random_game.make_next_move()
        else:
            moves = random_game.game.get_possible_moves()[0]
            random_game.move(moves[0], moves[1])

    winner = random_game.game.get_winner()
    assert winner is 1 or winner is 2 or winner is None


def test_min_max_game():
    min_max_game = MinMax(1, 5)

    while not min_max_game.game.is_over():

        if min_max_game.game.whose_turn() == 1:
            min_max_game.make_next_move()
        else:
            moves = min_max_game.game.get_possible_moves()[0]
            min_max_game.move(moves[0], moves[1])

    winner = min_max_game.game.get_winner()

    assert winner is 1


def test_hard_game():
    min_max_game = MinMax(1, 10)

    while not min_max_game.game.is_over():

        if min_max_game.game.whose_turn() == 1:
            min_max_game.make_next_move()
        else:
            moves = min_max_game.game.get_possible_moves()[0]
            min_max_game.move(moves[0], moves[1])

    winner = min_max_game.game.get_winner()

    assert winner is 1


test_min_max_game()
