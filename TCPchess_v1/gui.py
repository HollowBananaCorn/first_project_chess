import tkinter as tk
from Chess import *



class ChessGUI:
    def __init__(self, root, game):
        root.title("chess game")
        self.square_size = 20  #plz dont go above 25
        self.board_size = self.square_size * 8
        self.root = root 
        self.game = game
        self.canvas = tk.Canvas(root, width=self.board_size, height=self.board_size)
        self.canvas.pack()
        root.geometry(f"{self.board_size}x{self.board_size}")
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                colour = "white" if (row + col) % 2 == 0 else "gray"
                x0, y0 = col * self.square_size, row * self.square_size
                x1, y1 = (col + 1) * self.square_size, (row+ 1) * self.square_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colour)

    def update_board(self):
        self.draw_board()
        for row in range(8):
            for col in range(8):
                piece = self.game.board[col, row]
                if piece:
                    symbol = PIECE_UNICODE.get((piece.colour.value, piece.type.value))
                    x = col * self.square_size + (self.square_size / 2) #piece goes in the middle of the square
                    y = row * self.square_size + (self.square_size / 2)
                    self.canvas.create_text(x, y, text=symbol, font=("Arial", 30)) 

