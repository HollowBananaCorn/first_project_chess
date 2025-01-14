from Chess import *

def main():
    game = Game("1", "2")

    game1 = [
        "f2->f3", "e7->e6",
        "g2->g4", "d8->h4"
    ]
    game2 = [
        "e2->e4", "g7->g6",
        "d2->d4", "e7->e6",
        "g1->f3", "g8->e7",
        "h2->h4", "h7->h6",
        "c1->f4", "f8->g7",
        "d1->d2", "d7->d5",
        "e4->e5", "c7->c5",
        "c2->c3", "b8->c6",
        "b1->a3", "e8->f8",
        "d4->c5", "b7->b6",
        "c5->b6", "d8->b6",
        "f1->d3", "c8->a6",
        "b2->b4", "d5->d4",
        "b4->b5", "d4->c3",
        "d2->e3", "e7->d5",
        "e3->b6", "a7->b6",
        "b5->a6", "d5->f4",
        "d3->e4", "a8->a6",
        "e4->c6", "a6->a3",
        "e1->a1"           #limitations of testing: program relies on server for special moves. Promotion and castle impossible to do with just Chess class, promotion also requires user's answer. 
    ]


    moves = game1
    print(moves)
    i = 0
    while not game.end and i < len(moves):
        move = moves[i]
        print(move)
        if game.checkValid(move):
            game.makeMove(move)
        else:
            raise ValueError(f"invalid move: {move}")
        i+=1

    game.displayBoard()
    print(game.end)


if __name__ == "__main__":
    main()
