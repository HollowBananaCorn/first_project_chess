#launch first with something like /server.py 2000 

import socket
import sys

from Chess import *
from threading import Thread

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def validateMove(move, socket, game): # requests move until a valid one is entered


    while not game.checkValid(move):
        socket.sendall("EVENT invalid".encode() + b'\n')
        move = socket.recv(4096).decode().strip()

    messege = game.checkValid(move)
    if messege == "promotion":
        socket.sendall("EVENT promotion".encode() + b'\n')
        piece_responce = socket.recv(4096).decode().strip()
        if piece_responce == "B":
            piece = "B"
        elif piece_responce == "Q":
            piece = "Q"
        elif piece_responce == "R":
            piece = "R"
        else:
            piece = "H"
        messege = f"{messege}#{piece}"
        
    return move if type(messege) == bool else f"{move},{messege}"

def fight(addr1, sock1, addr2, sock2): # start the fight between 2 clients
	
	# first waiting player is white
	sock1.sendall("You are white".encode() + b'\n' + addr2.encode())
	sock2.sendall("You are black".encode() + b'\n' + addr1.encode())

	black_confirmation = sock2.recv(4096).decode().strip()
	if black_confirmation != "waiting for move":
		pass # quit (i'll change it out later)
	
	game = Game(addr1, addr2) #initialize the game instance


	while True: #send moves between clients untill game finishes

		game.displayBoard()
		move = sock1.recv(4096).decode().strip()
		move = validateMove(move, sock1, game)
		game.makeMove(move)
		if game.end:
			sock1.sendall("EVENT end".encode() + b'\n')
			sock2.sendall(f"EVENT end {move}".encode() + b'\n')
			break

		sock2.sendall(move.encode() + b'\n') #send move to black

		game.displayBoard()
		move = sock2.recv(4096).decode().strip()
		move = validateMove(move, sock2, game)
		game.makeMove(move)
		if game.end:
			sock1.sendall(f"EVENT end {move}".encode() + b'\n')
			sock2.sendall("EVENT end".encode() + b'\n')
			break

		sock1.sendall(move.encode() + b'\n') #send move to white 

	#game finighed, wait and send results
	final_confirmation1 = sock1.recv(4096).decode().strip()
	final_confirmation2 = sock2.recv(4096).decode().strip()

	if game.end == "Draw":
		sock1.sendall("Tie!".encode() + b'\n')
		sock2.sendall("Tie!".encode() + b'\n')
	elif game.end == "white lost":
		sock1.sendall("You lost".encode() + b'\n')
		sock2.sendall("You won".encode() + b'\n')
	else:
		sock1.sendall("You won".encode() + b'\n')
		sock2.sendall("You lost".encode() + b'\n')
	print(f"{addr1} and {addr2} finished fighting")
	sock1.close()
	sock2.close()




		



try:
	srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
	srv_sock.listen(5)
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)


current_waiting_addr = "" # the waiting client
current_waiting_sock = None

# Loop forever (or at least for as long as no fatal errors occur)
while True:

	print("Waiting for new client... ")
	
	cli_sock, cli_addr = srv_sock.accept()
	cli_addr_str = str(cli_addr) # Translate the client address to a string (to be used shortly)

	if current_waiting_addr == "":
		current_waiting_addr = cli_addr_str
		current_waiting_sock = cli_sock
		print("Client " + cli_addr_str + " connected. and waiting for another...")
	else:
		print("Client " + cli_addr_str + " connected. and started to fight with " + current_waiting_addr)

		thread = Thread(target = fight, args= (current_waiting_addr, current_waiting_sock, cli_addr_str, cli_sock))
		thread.start()

		current_waiting_addr = ""
		current_waiting_sock = None


# Close the server socket as well to release its resources back to the OS
srv_sock.close()

# Exit with a zero value, to indicate success
exit(0)



