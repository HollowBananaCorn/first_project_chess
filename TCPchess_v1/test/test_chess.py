from Chess import *

def test_innit_board() -> None:
    game = Game("white", "black")
    black_count = 0
    white_count = 0
    for i in range(8):
        for j in range(8):
            if game.board[i, j]:
                if game.board[i, j].colour == Colour.WHITE:
                    white_count +=1
                elif game.board[i, j].colour == Colour.BLACK:
                    black_count +=1

    if black_count != 16:
        raise AssertionError("there must be 16 black pieces")
    if white_count != 16:
        raise AssertionError("there must be 16 white pieces")
    assert True

def test_empty_board() -> None:
    board = Game.create_empty_board()

    for i in range(8):
        for j in range(8):
            if board[i, j]:
                raise AssertionError("board is not empty")
    assert True

# rook on empty board
def test_attack_empty_rook() -> None:
    board = Game.create_empty_board()

    for i in range(8):
        for j in range(8):
            board[i, j] = Piece(Colour.BLACK, PieceType.ROOK)
            squares = Game.attacks(board, i, j)
            if len(squares) != 14:
                raise AssertionError(f"Rook at coords {i} {j} attacks {len(squares)} squares, should be 14. Attacked: {squares}")
            board[i, j] = None
    assert True

# king on empty board
def test_attack_empty_corner_king()->None:
    board = Game.create_empty_board()
    board[0, 0] = Piece(Colour.BLACK, PieceType.KING)
    assert(len(Game.attacks(board, 0,0)) == 3)

def test_attack_empty_side_king()->None:
    board = Game.create_empty_board()
    board[5, 0] = Piece(Colour.BLACK, PieceType.KING)
    assert(len(Game.attacks(board, 5, 0)) == 5)

def test_attack_empty_middle_king()->None:
    board = Game.create_empty_board()
    board[4, 4] = Piece(Colour.BLACK, PieceType.KING)
    assert(len(Game.attacks(board, 4, 4)) == 8)

# bishop on empty board
def test_attack_empty_corner_bishop()->None:
    board = Game.create_empty_board()
    board[0, 0] = Piece(Colour.BLACK, PieceType.BISHOP)
    assert(len(Game.attacks(board, 0,0)) == 7)

def test_attack_empty_side_bishop()->None:
    board = Game.create_empty_board()
    board[5, 0] = Piece(Colour.BLACK, PieceType.BISHOP)
    assert(len(Game.attacks(board, 5, 0)) == 7)

def test_attack_empty_middle_bishop()->None:
    board = Game.create_empty_board()
    board[4, 4] = Piece(Colour.BLACK, PieceType.BISHOP)
    assert(len(Game.attacks(board, 4, 4)) == 13)

# Queen on empty board
def test_attack_empty_corner_Queen()->None:
    board = Game.create_empty_board()
    board[0, 0] = Piece(Colour.BLACK, PieceType.QUEEN)
    assert(len(Game.attacks(board, 0,0)) == 21)

def test_attack_empty_side_Queen()->None:
    board = Game.create_empty_board()
    board[5, 0] = Piece(Colour.BLACK, PieceType.QUEEN)
    assert(len(Game.attacks(board, 5, 0)) == 21)

def test_attack_empty_middle_Queen()->None:
    board = Game.create_empty_board()
    board[4, 4] = Piece(Colour.BLACK, PieceType.QUEEN)
    assert(len(Game.attacks(board, 4, 4)) == 27)

#pawn on empty board
def test_attack_empty_middle_pawn()->None:
    board = Game.create_empty_board()
    board[4, 4] = Piece(Colour.BLACK, PieceType.PAWN)
    assert(len(Game.attacks(board, 4, 4)) == 2)

def test_attack_empty_middle_pawn()->None:
    board = Game.create_empty_board()
    board[0, 4] = Piece(Colour.BLACK, PieceType.PAWN)
    assert(len(Game.attacks(board, 0, 4)) == 1)

def test_square_attacked_empty() -> None:
    empty_board = Game.create_empty_board()
    assert Game.isSquareAttacked(empty_board, 0, 0, Colour.WHITE) == False

def test_en_passant() -> None:

    game = Game("white", "black")

    game.makeMove("e2->e4")
    game.makeMove("d7->d5")
    game.makeMove("e4->d5")
    game.makeMove("e7->e5")
    
    assert game.sees(3, 4) == [(3, 5), (4, 5, 'en passant#1')] #can move forward or en passant to the right

def test_castle() -> None:
    game = Game("white", "black")

    board = game.create_empty_board()
    board[4, 0] = Piece(Colour.WHITE, PieceType.KING) #king E1
    board[0, 0] = Piece(Colour.WHITE, PieceType.ROOK) #rook A1
    board[7, 0] = Piece(Colour.WHITE, PieceType.ROOK) #king H1
    game.set_board(board)

    assert set(game.sees(4, 0)) - set(game.attacks(board, 4, 0)) == set([(0, 0, 'castle#long'), (7, 0, 'castle#short')])

def test_cant_castle_attacked() -> None:

    game = Game("white", "black")

    board = game.create_empty_board()
    board[4, 0] = Piece(Colour.WHITE, PieceType.KING) #king E1
    board[0, 0] = Piece(Colour.WHITE, PieceType.ROOK) #rook A1
    board[7, 0] = Piece(Colour.WHITE, PieceType.ROOK) #king H1
    board[5, 1] = Piece(Colour.BLACK, PieceType.BISHOP) #king is under attack
    
    game.set_board(board)

    assert not (set(game.sees(4, 0)) - set(game.attacks(board, 4, 0))) #king can't castle

def test_cant_castle_path_attacked() -> None:

    game = Game("white", "black")

    board = game.create_empty_board()
    board[4, 0] = Piece(Colour.WHITE, PieceType.KING) #king E1
    board[0, 0] = Piece(Colour.WHITE, PieceType.ROOK) #rook A1
    board[7, 0] = Piece(Colour.WHITE, PieceType.ROOK) #king H1
    board[4, 2] = Piece(Colour.BLACK, PieceType.BISHOP) #both castling paths are under attack
    
    game.set_board(board)

    assert not (set(game.sees(4, 0)) - set(game.attacks(board, 4, 0))) #king can't castle

def test_dame_over() -> None:

    game = Game("white", "black")

    game.makeMove("f2->f3")
    game.makeMove("d7->d6")
    game.makeMove("g2->g4")
    game.makeMove("c8->h4")
    
    assert game.is_game_over()