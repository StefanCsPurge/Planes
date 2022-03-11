# Planes
The Planes game. Exe file provided.

https://ro.wikipedia.org/wiki/Avioane_(joc)

Python implementation (with both CLI and GUI) of a 2-player
game in which each player sets his/her planes at the beginning in
a matrix, then tries to guess and attack the other’s planes in the
second matrix. If the cockpit is hit, the entire plane goes down.
The winner takes down all the opponent’s planes.

The human player has the computer as a worthy opponent which
plays its best move, each taking one turn.

The computer uses Graph Algorithms like BFS to find the next
move in case the last one was successful. Otherwise it hits a
random cell until a plane part is found, remembering not to hit
the same cell again.
