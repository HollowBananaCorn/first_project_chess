#launch twice with something like /client.py localhost 2000          


import socket
import sys



def make_turn(socket):
	while True:
		user_input = input("Your move: ").strip()  # Get the user's move
		socket.sendall(user_input.encode() + b'\n')

		opponent_move = socket.recv(4096).decode().strip()
		if opponent_move.startswith("EVENT"):
			messege = opponent_move.split()
			print(messege)
			if messege[1] == "invalid":
				print("Impossible move, try again")
			elif messege[1] == "promotion":
				print("""which piece would you like to promote to?
					   Q for Queen
					   B for Bishop
					   R for Rook
					   H for horsey""")  # Get the user's move
			elif messege[1] == "end":
				if len(messege) > 2:
					print("Opponent: " + messege[2])
				break
		else:
			print("Opponent: " + opponent_move)

	socket.sendall("waiting for results".encode() + b'\n')

	print(socket.recv(4096).decode().strip())



# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
srv_addr = (sys.argv[1], int(sys.argv[2])) # sys.argv[x] is the x'th argument on the command line

# Convert to string, to be used shortly
srv_addr_str = str(srv_addr)


try:
	print("Connecting to " + srv_addr_str + "... ")
	cli_sock.connect(srv_addr)
	
	print("Connected. Waiting for worthy opponent...")
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

"""
 Surround the following code in a try-except block to account for
 socket errors as well as errors related to user input. Ideally
 these error conditions should be handled separately.
"""
try:
	colour, opponent = cli_sock.recv(4096).decode().split("\n") # Receive and decode the colour
	

	if colour == "You are white":
		white = True
		

	elif colour == "You are black":
		white = False

	print("you are fighting as " + colour + ". Your opponet is: " + opponent)

	if white:
		make_turn(cli_sock)
	else:
		cli_sock.sendall("waiting for move".encode() + b'\n')

		first_white_turn = cli_sock.recv(4096).decode().strip()

		if not first_white_turn.startswith("EVENT end"):
			print("Opponent: " + first_white_turn)
			make_turn(cli_sock)
finally:
	"""
	 If an error occurs or the server closes the connection, call close() on the
	 connected socket to release the resources allocated to it by the OS.
	"""
	cli_sock.close()

# Exit with a zero value, to indicate success
exit(0)






