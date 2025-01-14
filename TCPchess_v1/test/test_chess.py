from Chess import *

def test_attack_default() -> None:
    new_board = Game("white", "black")
    assert new_board.attacks(new_board.board,  0, 0) == [(1, 0), (0, 1)]

    empty_board = np.full((8, 8), None, dtype=object)
    assert Game.attacks(empty_board, 4, 4) == []

    empty_board[0, 0] = Piece(Colour.WHITE, PieceType.QUEEN)
    assert Game.attacks(empty_board, 0, 0) == [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]

    empty_board[0, 0] = Piece(Colour.WHITE, PieceType.HORSE)
    assert Game.attacks(empty_board, 0, 0) == [(1, 2), (2, 1)]

    empty_board[0, 0] = Piece(Colour.WHITE, PieceType.KING)
    assert set(Game.attacks(empty_board, 0, 0)) == {(1, 0), (1, 1), (0, 1)}


def test_square_attacked() -> None:
    empty_board = np.full((8, 8), None, dtype=object)
    assert Game.isSquareAttacked(empty_board, 0, 0, Colour.WHITE) == False
