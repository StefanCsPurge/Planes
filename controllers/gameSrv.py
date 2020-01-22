from domain.board import Board
from domain.plane import Plane,PlaneValidator,PlaneError
import random

class GameService:
    def __init__(self):
        """
        Constructor of the game controller class.
        """
        self.__playerBoard = Board(8,8).getMatrix()
        self.__computerBoard = Board(8,8).getMatrix()
        self.__hitBoard = Board(8,8).getMatrix()
        self.__computerPlanes = []
        self.__playerPlanes = []
        self.__computerMoves = [(0,0),(0,7),(7,0),(7,7)]
        self.__neighboursQueue = []
        self.addComputerPlanes()

    def resetGame(self):
        """
        Method that resets all the game progress by calling the initializer of the controller class.
        """
        self.__init__()

    def getPlayerBoard(self):
        """
        Getter for the matrix that contains the player's planes.
        :return: list of lists - the matrix described above
        """
        return self.__playerBoard[:][:]

    def getComputerBoard(self):
        """
        Getter for the matrix that contains the computer's planes.
        :return: list of lists - the matrix described above
        """
        return self.__computerBoard[:][:]

    def getHitBoard(self):
        """
        Getter for the matrix where the player player shoots.
        :return: list of lists - the matrix described above
        """
        return self.__hitBoard[:][:]

    def getWinner(self):
        """
        Method that gets the winner of the game by checking if a player is out of planes.
        :return: str - the winner: human or computer
        """
        winner = None
        if not len(self.__computerPlanes):
            winner = 'human'
        elif not len(self.__playerPlanes):
            winner = 'computer'
        return winner

    def addPlayerPlane(self,cabinPos,orientation):
        """
        Method used to add a human player's plane to his board.
        :param cabinPos: tuple with 2 int values - the coordinates of the plane cabin in the matrix
        :param orientation: str - up/down/left/right: the plane orientation
        """
        plane = Plane(cabinPos, orientation)
        PlaneValidator.validate(plane,self.__playerBoard)
        planeCells = plane.getPlaneCells()
        for cell in planeCells:
            self.__playerBoard[cell[0]][cell[1]] = '#'
        self.__playerPlanes.append(plane)

    def addComputerPlanes(self):
        """
        Method that adds 2 random and valid planes to the computer's board.
        """
        addedPlanes = 0
        while addedPlanes < 2:
            try:
                cabPos = (random.randint(0,7),random.randint(0,7))
                orientation = random.choice(["up", "down", "left", "right"])
                plane = Plane(cabPos, orientation)
                PlaneValidator.validate(plane, self.__computerBoard)
                planeCells = plane.getPlaneCells()
                for cell in planeCells:
                    self.__computerBoard[cell[0]][cell[1]] = '#'
                self.__computerPlanes.append(plane)
                addedPlanes += 1
            except PlaneError:
                pass

    @staticmethod
    def markDestroyedPlane(plane,board):
        """
        Static method used to mark a destroyed plane's cells with 'X's on a board.
        :param plane: Plane object
        :param board: list of lists (matrix)
        :return:
        """
        planeCells = plane.getPlaneCells()
        for c in planeCells:
            board[c[0]][c[1]] = 'X'

    def playerHit(self,hitPosition):
        """
        Method that gets the result of the human player hit and marks it on the hit board & computer's board.
        :param hitPosition: tuple with the hit coordinates in the matrix
        :return: str - cabin/hit/miss
        """
        for plane in self.__computerPlanes:
            if plane.getCabinPosition() == hitPosition:
                self.markDestroyedPlane(plane,self.__computerBoard)
                self.markDestroyedPlane(plane,self.__hitBoard)
                self.__computerPlanes.remove(plane)
                return 'cabin'
        row = hitPosition[0]
        col = hitPosition[1]
        if self.__computerBoard[row][col] == '#':
            self.__hitBoard[row][col] = 'X'
            self.__computerBoard[row][col] = 'X'
            return 'hit'
        self.__hitBoard[row][col] = 0
        return 'miss'

    def __addDestroyedCellsToMoves(self,plane):
        """
        Method that adds a destroyed plane's cells to the computer moves list,
        so they won't be visited again by the computer
        :param plane: Plane object
        """
        for c in plane.getPlaneCells():
            self.__computerMoves.append(c)

    def __getRandomUnvisitedCell(self):
        """
        Method that that gets a random unvisited cell by the computer.
        :return: hitPos - tuple that contains the coordinates of the cell
        """
        hitPos = None
        while hitPos is None:
            row = random.randint(0, 7)
            col = random.randint(0, 7)
            hitPos = (row, col)
            if hitPos in self.__computerMoves:
                hitPos = None
        return hitPos

    def __getComputerMove(self):
        """
        Method that gets the next computer move/hit.
        :return: hitPos - tuple that contains the coordinates of the cell to be hit
        """
        if not len(self.__neighboursQueue):
            hitPos = self.__getRandomUnvisitedCell()
        else:
            hitPos = self.__neighboursQueue.pop(0)
        self.__computerMoves.append(hitPos)
        return hitPos

    def __goodCell(self,row,col):
        """
        Method checks if the cell's coordinates are inside the matrix and unvisited.
        :param row: int - the cell row
        :param col: int - the cell column
        :return: True/False
        """
        condition1 = row in range(8) and col in range(8)
        condition2 = (row,col) not in self.__computerMoves
        return condition1 and condition2

    def __enqueueNeighbours(self,row,col):
        """
        Method that adds the neighbours of a cell in the queue used by the computer
        to hit cells near a successful shot.
        :param row: int - the cell row
        :param col: int - the cell column
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for d in directions:
            if self.__goodCell(row+d[0],col+d[1]):
                self.__neighboursQueue.append((row+d[0],col+d[1]))

    def computerHit(self):
        """
        Method that gets the result of the computer hit and marks it on the player's board.
        The neighbours queue is modified in case of a successful shot accordingly.
        :return: str - cabin/hit/miss
        """
        hitPos = self.__getComputerMove()
        row = hitPos[0]
        col = hitPos[1]
        for plane in self.__playerPlanes:
            if plane.getCabinPosition() == hitPos:
                self.markDestroyedPlane(plane,self.__playerBoard)
                self.__addDestroyedCellsToMoves(plane)
                self.__playerPlanes.remove(plane)
                self.__neighboursQueue.clear()
                return 'cabin'
        if self.__playerBoard[row][col] == '#':
            self.__playerBoard[row][col] = 'X'
            self.__enqueueNeighbours(row,col)
            return 'hit'
        self.__playerBoard[row][col] = 0
        return 'miss'
