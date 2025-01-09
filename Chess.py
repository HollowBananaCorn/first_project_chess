from enum import Enum
from copy import copy, deepcopy
from re import match
import numpy as np

class Colour(Enum):
    WHITE = "white"
    BLACK = "black"

class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    HORSE = "horse"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class Piece:
    
	def __init__(self, colour: Colour, type: PieceType):
		self.colour = colour
		self.type = type

		

	def __str__(self):
		return f"{self.colour.value} {self.type.value}"
	
# class Pawn(Piece):  #thought i might add this, decided its not that important for python, will do  it in java instead.
# 	def __init__(self, colour: Colour):
# 		super().__init__(colour, PieceType.PAWN)

# 		self.did_double_move = False


class Game:

	def __init__(self, white: str, black: str):
		self.white = white #id or addresses of each player
		self.black = black
		self.end = None
		

		# make an empty 8x8 board
		self.board = np.full((8, 8), None, dtype=object)

		# set up the starting position
		self.initialize_start_board()

		self.positions = [self.board]
		self.turn = Colour.WHITE
		
		
	def initialize_start_board(self):
		for i in range(8): #pawns
			self.board[i, 1] = Piece(Colour.WHITE, PieceType.PAWN)
			self.board[i, 6] = Piece(Colour.BLACK, PieceType.PAWN)

		#white pieces
		self.board[0, 0] = Piece(Colour.WHITE, PieceType.ROOK)
		self.board[1, 0] = Piece(Colour.WHITE, PieceType.HORSE)
		self.board[2, 0] = Piece(Colour.WHITE, PieceType.BISHOP)
		self.board[3, 0] = Piece(Colour.WHITE, PieceType.QUEEN)
		self.board[4, 0] = Piece(Colour.WHITE, PieceType.KING)
		self.board[5, 0] = Piece(Colour.WHITE, PieceType.BISHOP)
		self.board[6, 0] = Piece(Colour.WHITE, PieceType.HORSE)
		self.board[7, 0] = Piece(Colour.WHITE, PieceType.ROOK)

		# black pieces
		self.board[0, 7] = Piece(Colour.BLACK, PieceType.ROOK)
		self.board[1, 7] = Piece(Colour.BLACK, PieceType.HORSE)
		self.board[2, 7] = Piece(Colour.BLACK, PieceType.BISHOP)
		self.board[3, 7] = Piece(Colour.BLACK, PieceType.QUEEN)
		self.board[4, 7] = Piece(Colour.BLACK, PieceType.KING)
		self.board[5, 7] = Piece(Colour.BLACK, PieceType.BISHOP)
		self.board[6, 7] = Piece(Colour.BLACK, PieceType.HORSE)
		self.board[7, 7] = Piece(Colour.BLACK, PieceType.ROOK)

	def sees(self, l, n): #all squeres a piece can see
		squares = []

		pieceType = self.board[l, n].type
		#print(pieceType)
		if pieceType == None:
			return squares
		elif pieceType == PieceType.KING:
			possibles = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, -1), (1, 0)]

			for (i, j) in possibles:
				new_letter = l+i
				new_number = n+j
				if 0<= new_letter < 8 and 0<= new_number < 8: #checks if in board bounds
					if not self.board[new_letter, new_number] or self.board[new_letter, new_number].colour != self.board[l, n].colour: #checks if lands on empty square or racially motivated (typical monark).
						squares.append((new_letter, new_number))

			#castle possibilities(by general Fisher Chess)(to castle, the king must go to the square of the rook):
			if not self.isSquareAttacked(self.board, l, n, self.turn):
				king_moved = False
				for position in self.positions:
					if not position[l, n] or position[l, n].type != PieceType.KING:
						king_moved = True
				
				if not king_moved:
					#find original Queenside Rook
					i = l
					while i >= 0:
						if self.positions[0][i, j] and self.positions[0][i, j].type == PieceType.ROOK:
							break
						i -= 1
					#i - letter index of rook
					#l - letter index of king
					rookQ_moved = False
					if i != -1:
						for position in self.positions:
							if position[i, n].type != PieceType.ROOK:
								rookQ_moved = True
					
					if not rookQ_moved:
						#first, if king is on b square
						if l == 1:
							if not self.isSquareAttacked(self.board, 2, n, self.turn) and not self.board[2, n] and not self.board[3, n]:
								squares.append((i, n, "castle#long"))
						else:
							#King must be able to move to c square.
							castle_king_path_valid = True
							current_square_check = 2 #letter 'c' on the board
							while current_square_check < l:
								if current_square_check == i: #fine if the rook on path, but not fine if it is attacked
									if self.isSquareAttacked(self.board, current_square_check, n, self.turn):
										castle_king_path_valid = False
								else: 
									if self.isSquareAttacked(self.board, current_square_check, n, self.turn) or self.board[current_square_check, n]:
										castle_king_path_valid = False # not fine if other square is non-empty or under attack
								current_square_check+=1
							
							if castle_king_path_valid:
								# now check if space for rook moves:
								castle_rook_path_valid = True
								current_square_check = 3 #letter 'f' on the board
								if 2 > i:
									while current_square_check > i:
										if current_square_check == l:
											pass #skip the king
										elif self.board[current_square_check, n] != None:
											castle_rook_path_valid = False # if piece in the way, return false
										current_square_check -= 1
								elif i >= 4:
									while current_square_check < i:
										if self.board[current_square_check, n]:
											castle_rook_path_valid = False
								
								if castle_rook_path_valid:
									squares.append((i, n, "castle#long"))

					#now do the same for kingside rook
					i = l
					while i < 8:
						if self.positions[0][i, j] and self.positions[0][i, j].type == PieceType.ROOK:
							break
						i += 1
					#i - letter index of rook
					#l - letter index of king
					rookK_moved = False
					if i != 8:
						for position in self.positions:
							if position[i, n].type != PieceType.ROOK:
								rookK_moved = True
						
					if not rookK_moved:
						castle_king_path_valid = True
						current_square_check = 6 #letter 'g' on the board
						while current_square_check > l:
							if current_square_check == i: #fine if the rook on path, but not fine if it is attacked
								if self.isSquareAttacked(self.board, current_square_check, n, self.turn):
									castle_king_path_valid = False
							else: 
								if self.isSquareAttacked(self.board, current_square_check, n, self.turn) or self.board[current_square_check, n]:
									castle_king_path_valid = False # not fine if other square is non-empty or under attack
							current_square_check-=1
						if castle_king_path_valid: #we dont need to check rook's path because it's all checked while doing the king's path.
							squares.append((i, n, "castle#short"))
				

		elif pieceType == PieceType.HORSE:
			possibles = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, -1), (2, 1)]

			for (i, j) in possibles:
				new_letter = l+i
				new_number = n+j
				if 0<= new_letter < 8 and 0<= new_number < 8:
					if not self.board[new_letter, new_number] or self.board[new_letter, new_number].colour != self.board[l, n].colour:
						squares.append((new_letter, new_number))


		elif pieceType == PieceType.ROOK:
			#positive x
			i = l+1
			while i < 8 and not self.board[i, n]: #append untill end of board or piece in the way
				squares.append((i, n))
				i+=1
			if i < 8 and self.board[i, n].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, n))

			#positive y
			j = n+1
			while j < 8 and not self.board[l, j]: #append untill end of board or piece in the way
				squares.append((l, j))
				j+=1
			if j < 8 and self.board[l, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((l, j))

			#negative x
			i = l-1
			while i >= 0 and not self.board[i, n]: #append untill end of board or piece in the way
				squares.append((i, n))
				i-=1
			if i >= 0 and self.board[i, n].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, n))

			#negative y
			j = n-1
			while j >= 0 and not self.board[l, j]: #append untill end of board or piece in the way
				squares.append((l, j))
				j-=1
			if j >= 0 and self.board[l, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((l, j))
		
		elif pieceType == PieceType.BISHOP:
			#45
			i = l+1
			j = n+1
			while i < 8 and j < 8 and not self.board[i, j]: #append untill end of board or piece in the way
				squares.append((i, j))
				i+=1
				j+=1
			if i < 8 and j <8 and self.board[i, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, j))

			#135
			i = l-1
			j = n+1
			while i >= 0 and j < 8 and not self.board[i, j]: #append untill end of board or piece in the way
				squares.append((i, j))
				i-=1
				j+=1
			if i >= 0 and j < 8 and self.board[i, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, j))

			#225
			i = l-1
			j = n-1
			while i >= 0 and j >= 0 and not self.board[i, j]: #append untill end of board or piece in the way
				squares.append((i, j))
				i-=1
				j-=1
			if i >= 0 and j >= 0 and self.board[i, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, j))

			#315
			i = l+1
			j = n-1
			while i < 8 and j >= 0 and not self.board[i, j]: #append untill end of board or piece in the way
				squares.append((i, j))
				i+=1
				j-=1
			if i < 8 and j >= 0 and self.board[i, j].colour != self.board[l, n].colour: # add to list if you can take that piece
				squares.append((i, j))

		elif pieceType == PieceType.QUEEN:
			#calculate the squares by exxchanging it to a rook, a biachop, and then adding the squares and returning it back to a queen
			newRook = Piece(self.board[l, n].colour, PieceType.ROOK)
			newBishop = Piece(self.board[l, n].colour, PieceType.BISHOP)

			self.board[l, n] = newRook
			straight_squares = self.sees(l, n)

			self.board[l, n] = newBishop
			gay_squares = self.sees(l, n)

			self.board[l, n] = Piece(self.board[l, n].colour, PieceType.QUEEN)
			squares = gay_squares + straight_squares

		elif pieceType == PieceType.PAWN:
			direction = 1 if self.board[l, n].colour == Colour.WHITE else -1

			if  not self.board[l, n + direction]: #checks if pieces on path straight ahead
				if n+direction in (0, 7): #if pawn going to promote
					squares.append((l, n+direction, "promotion"))
				else:
					squares.append((l, n + direction))
					if n-direction in (0, 7) and not self.board[l, n + 2*direction]: #if on second rank, allow double move
						squares.append((l, n + 2*direction))

			for i in (-1, 1): #checks if it can take
				if 0 <= l+i < 8:
					if self.board[l+i, n+direction] and self.board[l, n].colour != self.board[l+i, n+direction].colour:
						if n+direction in (0, 7): #if pawn going to promote
							squares.append((l+i, n+direction, "promotion"))
						else:
							squares.append((l+i, n+direction))

					elif (direction == 1 and n == 4) or (direction == -1 and n == 3):#pawn in in possible row for en passant
						if self.board[l+i, n] and self.board[l, n].colour != self.board[l+i, n].colour and self.board[l+i, n].type == PieceType.PAWN and not self.board[l+i, n+2*direction] and not self.positions[-2][l+i, n] and self.positions[-2][l+i, n+2*direction] and self.positions[-2][l+i, n+2*direction].type == PieceType.PAWN:
							# if next to the pawn is a pawn of opposite colour and in the previous move, it moved 2 squares, leaving the original square empty, en passant
							squares.append((l+i, n+direction, f"en passant#{i}"))

		#now check if the move will result in your king being checked
		actually_valid_squares = []
		for square in squares:
			new_position = deepcopy(self.board)
			if len(square) == 2 or square[2] == "promotion":
				new_position[l, n] = None
				new_position[square[0], square[1]] = self.board[l, n]
					
			elif square[2].startswith("en passant"):
				offset = int(square[2].split("#")[1])
				new_position[l, n] = None
				new_position[l+offset, n] = None        # Pawn that moved 2 squares gets eaten
				new_position[square[0], square[1]] = self.board[l, n]

			elif square[2].startswith("castle"):
				new_position[l, n] = None
				new_position[square[0], square[1]] = None
				if square[2].split("#")[1] == "long":
					new_position[2, n] = self.board[l, n] # place King at letter 'c'
					new_position[3, n] = self.board[square[0], n] # place rook at letter 'd'
				else:
					new_position[6, n] = self.board[l, n] # place King at letter 'g'
					new_position[5, n] = self.board[square[0], n] # place rook at letter 'f'

			if not self.isKingAttacked(new_position, self.turn):
				actually_valid_squares.append(square)
		return actually_valid_squares

	def checkValid(self, move):
		letters = "abcdefgh"
		numbers = "12345678"
		# example of a valid move:  e2->e4
		if len(move.split("->")) != 2: #placeholder condition
			return False
		
		sq1 , sq2 = move.split("->")
		if len(sq1)!= 2:
			return False

		letter = sq1[0]
		if letter not in letters:
			return False

		l1 = ord(letter) - ord('a') #a rray letter(horizontal) index square

		number = sq1[1]
		if number not in numbers:
			return False

		n1 = int(number) - 1 # array number(vertical) index of first square

		if len(sq2)!= 2:
			return False
		
		letter = sq2[0]
		if letter not in letters:
			return False

		l2 = ord(letter) - ord('a') # array letter(horizontal) index square

		number = sq2[1]
		if number not in numbers:
			return False

		n2 = int(number) - 1 #array number(vertical) index of target square

		
		print(f"starting square - ({l1}, {n1}), endin square - ({l2}, {n2})")

		if not self.board[l1, n1]:#makes sure there is a piece on the board
			return False

		print("first square:")
		print(self.board[l1, n1].type, self.board[l1, n1].colour)
		#turn = Colour.WHITE if len(self.positions) % 2 == 1 else Colour.BLACK

		if self.board[l1, n1].colour != self.turn:
			return False
		print("possible moves:")
		print(self.sees(l1, n1))
		#if (l2, n2) not in self.sees(l1, n1):
		#	return False
		
		# if that move is visible for the piece on the original square, returns true or extra information
		list_of_squares = self.sees(l1, n1)
		found = False
		for square in list_of_squares: #no while loop since short list
			if l2 == square[0] and n2 == square[1]:
				if len(square) == 2: #if only contains horisontal and vertical position, return true
					return True
				else:
					return square[2] #returns extra info of that move(if en passant or castle)

		
		print("move not valid")
		return found
	
	def makeMove(self, move):
		print(move)
		new_position = deepcopy(self.board)
		info = ""

		if "," in move:
			move, info = move.split(",")
		
		# move is in a e2->e4 format, so we need to get the array indexes from it
		sq1 , sq2 = move.split("->")
		letter = sq1[0]
		number = sq1[1]
		l1 = ord(letter) - ord('a')
		n1 = int(number) - 1
		letter = sq2[0]
		number = sq2[1]
		l2 = ord(letter) - ord('a')
		n2 = int(number) - 1

		if not info: # if normal move
			new_position[l1, n1] = None               # Original square becomes empty
			new_position[l2, n2] = self.board[l1, n1] # Piece moves to new square

		elif info.startswith("en passant"):
			offset = int(info.split("#")[1])
			new_position[l1, n1] = None
			new_position[l1+offset, n1] = None        # Pawn that moved 2 squares gets eaten
			new_position[l2, n2] = self.board[l1, n1]

		elif info.startswith("castle"):
			new_position[l1, n1] = None
			new_position[l2, n2] = None
			if info.split("#")[1] == "long":
				new_position[2, n1] = self.board[l1, n1] # place King at letter 'c'
				new_position[3, n2] = self.board[l2, n2] # place rook at letter 'd'
			else:
				new_position[6, n1] = self.board[l1, n1] # place King at letter 'g'
				new_position[5, n2] = self.board[l2, n2] # place rook at letter 'f'

		elif info.startswith("promotion"):
			piece = info.split("#")[1]
			match piece:
				case "B":
					to_promote = PieceType.BISHOP
				case "Q":
					to_promote = PieceType.QUEEN
				case "H":
					to_promote = PieceType.HORSE
				case "R":
					to_promote = PieceType.ROOK

			new_position[l1, n1] = None
			new_position[l2, n2] = Piece(self.board[l1, n1].colour, to_promote) # promote to piece with corresponding colour and type


		self.board = new_position
		self.positions.append(self.board)
		self.turn = Colour.BLACK if self.turn == Colour.WHITE else Colour.WHITE

		if self.is_game_over():
			if self.isKingAttacked(self.board, self.turn):
				self.end = f"{self.turn.value} lost"
			else:
				self.end = "Draw"


	@staticmethod
	def attacks(position, l, n):
		squares = []

		pieceType = position[l, n].type
		if pieceType == None:
			return squares
		elif pieceType == PieceType.KING:
			possibles = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, -1), (1, 0)]

			for (i, j) in possibles:
				new_letter = l+i
				new_number = n+j
				if 0<= new_letter < 8 and 0<= new_number < 8: #checks if in board bounds
					squares.append((new_letter, new_number))

		elif pieceType == PieceType.HORSE:
			possibles = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, -1), (2, 1)]

			for (i, j) in possibles:
				new_letter = l+i
				new_number = n+j
				if 0<= new_letter < 8 and 0<= new_number < 8:
					squares.append((new_letter, new_number))

		elif pieceType == PieceType.BISHOP:
			directions = [(1,1), (-1, 1), (-1, -1), (1, -1)]

			for letter, number in directions:
				new_letter, new_number = l, n
				while 0 <= new_letter+letter < 8 and 0 <= new_number+number < 8:
					new_letter+=letter
					new_number+=number
					squares.append((new_letter, new_number))
					if position[new_letter, new_number]: # if a piece blocks the way, stop attacking that direction.
						break
		
		elif pieceType == PieceType.ROOK:
			directions = [(1,0), (0, 1), (-1, 0), (0, -1)]

			for letter, number in directions:
				new_letter, new_number = l, n
				while 0 <= new_letter+letter < 8 and 0 <= new_number+number < 8:
					new_letter+=letter
					new_number+=number
					squares.append((new_letter, new_number))
					if position[new_letter, new_number]: # if a piece blocks the way, stop attacking that direction.
						break

		elif pieceType == PieceType.QUEEN:
			directions = [(1,0), (1,1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

			for letter, number in directions:
				new_letter, new_number = l, n
				while 0 <= new_letter+letter < 8 and 0 <= new_number+number < 8:
					new_letter+=letter
					new_number+=number
					squares.append((new_letter, new_number))
					if position[new_letter, new_number]: # if a piece blocks the way, stop attacking that direction.
						break

		elif pieceType == PieceType.PAWN:
			direction = 1 if position[l, n].colour == Colour.WHITE else -1
			for letter in (-1, 1):
				if 0<= l+letter < 8:
					squares.append((l+letter, n+direction))

		
		return squares
	
	@staticmethod
	def isSquareAttacked(position, letter, number, current_colour):
		# returns True if a square is attacked by a piece of the opposite colour. 
		for l in range(8):
			for n in range(8):
				if position[l, n] and position[l, n].colour != current_colour:
					#print(letter, number, l, n,  Game.attacks(position, l, n))
					if (letter, number) in Game.attacks(position, l, n): return True

		return False
	
	@staticmethod
	def isKingAttacked(position, colour):
		for i in range(8):
			for j in range(8):
				if position[i, j] and position[i, j].type == PieceType.KING and position[i, j].colour == colour:
					kLetter, kNumber = i, j

		#print(f"king at {kLetter}{kNumber}")
		#print(self.isSquareAttacked(kLetter, kNumber))
		return Game.isSquareAttacked(position, kLetter, kNumber, colour)

	def is_game_over(self):
		#checks if no legal moves remain
		for i in range(8):
			for j in range(8):
				if self.board[i, j] and self.board[i, j].colour == self.turn:
					if self.sees(i, j):
						return False  # if a valid move found, game continues

		return True

	def displayBoard(self):
		for row in self.board:
			print([str(piece) if piece else "Empty" for piece in row])