from texttable import Texttable

class Console:
    def __init__(self,planesService):
        self.__srv = planesService
        self.__menu = "Enter: [s] to start a new game | [x] to exit"
        self.__hitRes = {'cabin':"{} DESTROYED a plane!",'hit':"{} HIT a plane!",'miss':"{} MISSED!"}
        self.__bHeader = ['~', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def printTable(self,board):
        table = Texttable()
        table.header(self.__bHeader)
        for i in range(8):
            table.add_row([str(i+1)] + [board[i][j] for j in range(8)])
        print(table.draw()+'\n')

    @staticmethod
    def showPlane():
        print("""The cabin -> #          Example
         # # # # #      of plane
             #          heading 
           # # #        up\n""")

    @staticmethod
    def getColNr(col):
        return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].index(col.upper())

    def readCell(self,msg):
        """
        Function that reads a cell coordinates from the user input.
        :param msg: str - the message to be shown when reading the cell
        :return: tuple with the coordinates of the cell
        """
        while True:
            try:
                strCoord = input(msg).strip()
                if len(strCoord) != 2 or not strCoord[1].isdigit() or not strCoord[0].isalpha():
                    raise Exception
                cell = (int(strCoord[1]) - 1, self.getColNr(strCoord[0]))
                return cell
            except Exception as ex:
                print("Invalid coordinates! " + str(ex))

    def readPlane(self):
        cabPos = self.readCell("Insert cabin coordinates (eg: A4, E7 etc): ")
        while True:
            orientation = input("Where is the plane heading? (up/down/right/left): ").strip().lower()
            if orientation in ('up','down','right','left'):
                break
            else:
                print("Invalid plane orientation!")
        return cabPos, orientation

    def addPlayerPlanes(self):
        print("You must add 2 planes in the following grid; max plane width is 5 (wing-wing), max plane length is 4 (cabin-tail).")
        self.printTable(self.__srv.getPlayerBoard())
        self.showPlane()
        addedPlanes = 0
        while addedPlanes < 2:
            try:
                cabPos, orientation = self.readPlane()
                self.__srv.addPlayerPlane(cabPos, orientation)
                addedPlanes += 1
                if addedPlanes < 2:
                    self.printTable(self.__srv.getPlayerBoard())
            except Exception as ex:
                print(ex)

    def printBoards2(self,secondBoard,msg):
        b1 = self.__srv.getPlayerBoard()
        b2 = secondBoard
        table = Texttable()
        print("Your planes:{}{}:".format(' '*32,msg))
        table.header(self.__bHeader + ['<  >'] + self.__bHeader)
        for i in range(8):
            table.add_row([str(i + 1)] + [b1[i][j] for j in range(8)] + ['<  >'] + [str(i + 1)] + [b2[i][j] for j in range(8)])
        print(table.draw() + '\n')

    def showHitResults(self,playerHit,compHit):
        if compHit is None or playerHit is None:
            print("Let's start shooting !")
        else:
            print(self.__hitRes[playerHit].format('You'))
            print(self.__hitRes[compHit].format('Computer'))

    def newGame(self):
        self.__srv.resetGame()
        self.addPlayerPlanes()
        print('The computer placed its planes as well.')
        hitRes1 = hitRes2 = None
        while True:
            self.printBoards2(self.__srv.getHitBoard(), "Your shots")
            self.showHitResults(hitRes1,hitRes2)
            try:
                # Player's turn
                hitPos = self.readCell("\nInsert the cell you want to hit (eg: A4, E7 etc): ")
                hitRes1 = self.__srv.playerHit(hitPos)
                if self.__srv.getWinner() == 'human':
                    self.printBoards2(self.__srv.getComputerBoard(), "Computer's planes")
                    print("YOU HAVE WON!\n")
                    break

                # Computer's turn
                hitRes2 = self.__srv.computerHit()
                if self.__srv.getWinner() == 'computer':
                    self.printBoards2(self.__srv.getComputerBoard(), "Computer's planes")
                    print("GAME OVER! You have lost!\n")
                    break
            except Exception as ex:
                print(ex)

    def run(self):
        print("© © © © © ©  M. Ștefan C.  © © © © © ©")
        print("~ W E L C O M E   T O   P L A N E S ~\n")
        while True:
            print(self.__menu)
            choice = input('->').strip()
            try:
                if choice == 'x':
                    break
                if choice == 's':
                    self.newGame()
                else:
                    raise Exception("Invalid choice!")
            except Exception as ex:
                print(ex)
