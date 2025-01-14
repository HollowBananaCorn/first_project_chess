# first_project_chess


Very basic python project which i mostly did for myself as a baseline for a similar Java project.

After opening the server with a port number, for example server.py 2000, it waits for 2 clients to connect(with something like client.py localhost 2000) and starts a thread from them, which runs the chess game.
The first to connect always goes first. The imput would be "e2->e4". When Castling, your original square wouldbe your king, and the next one would be the position of the queen-side or king-side rook. This way it also works with chess 960. When promoting, The server asks the client which piece would they want to promote to, before finishing the move. If the imput as anything other than B, Q, R, the pawn promotes to a Horsey.

The Chess file by itself can do everything other than placing the pieces for Promotion and Castling correctly. When i shall do it in Java, i may add the possibility to write moves in the correct chess format, to be able to re-enact them.
