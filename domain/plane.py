class Plane:
    def __init__(self,cabinPosition,orientation):
        """
        Plane object constructor.
        :param cabinPosition: tuple that contains the coordinates of the cabin in the matrix
        :param orientation: str - up/down/left/right
        """
        self.__cabPos = cabinPosition  # tuple with the coordinates in the board matrix, eg: (0,2) - row and column
        self.__orientation = orientation
        self.__DirAndSign = self.getPlaneDirections(self.__orientation)

    def getCabinPosition(self):
        """
        Getter for the position of the plane cabin.
        :return: tuple that contains the coordinates of the cabin in the matrix
        """
        return self.__cabPos

    def getPlaneOrientation(self):
        """
        Getter for the plane orientation.
        :return: str - up/down/left/right
        """
        return self.__orientation

    @staticmethod
    def getPlaneDirections(orientation):
        """
        Method that gets the plane directions for its cells based on a given orientation.
        :param orientation: str - up/down/left/right
        :return: tuple that contains the corresponding cell directions and the sign used to iterate over the matrix
        """
        UpDownDirections = [(0, 0), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)]
        LeftRightDirections = [(0, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]
        DirAndSign = {'up': (UpDownDirections,1), 'down': (UpDownDirections,-1),
                      'left': (LeftRightDirections,1), 'right': (LeftRightDirections,-1)}
        return DirAndSign[orientation]

    def getPlaneCells(self):
        """
        Method that gets all the cells that the plane occupies on the board.
        :return: cells - list that contains all 10 cells of the plane
        """
        cells = []
        directions = self.__DirAndSign[0]
        sign = self.__DirAndSign[1]
        for d in directions:
            currentRow = self.__cabPos[0] + sign * d[0]
            currentCol = self.__cabPos[1] + sign * d[1]
            cells.append((currentRow,currentCol))
        return cells

class PlaneValidator:
    @staticmethod
    def validate(plane,board):
        """
        Static method used to validate a plane by checking its cabin position and the positioning on the board.
        :param plane: PLane objects
        :param board: list of lists - Board matrix
        :raises: PlaneError in case of invalid plane
        """
        cabPos = plane.getCabinPosition()
        if type(cabPos) is not tuple or len(cabPos) != 2 or cabPos[0] not in range(8) or cabPos[1] not in range(8):
            raise PlaneError('Invalid cabin position!')
        cells = plane.getPlaneCells()
        for cell in cells:
            if cell[0] not in range(8) or cell[1] not in range(8):
                raise PlaneError('Invalid plane positioning! The plane is outside the playing area!')
            if board[cell[0]][cell[1]] == '#':
                raise PlaneError('Invalid plane positioning! This plane overlaps the other plane!')

    @staticmethod
    def GUIValidate(selectedCells):
        """
        Static method used to validate a plane input from GUI, using the selected cells.
        In case of valid plane, it returns the cabin position and the orientation.
        :param selectedCells: list of cells
        :return: cabin position (tuple with the coordinates), direction (str - up/down/left/right)
        :raises: PlaneError in case of invalid plane
        """
        if len(selectedCells) != 10:
            raise PlaneError("Invalid plane!")
        UpDownDirections = [(0, 0), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)]
        LeftRightDirections = [(0, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]
        DirAndSign = {'up': (UpDownDirections, 1), 'down': (UpDownDirections, -1),
                      'left': (LeftRightDirections, 1), 'right': (LeftRightDirections, -1)}
        for d in DirAndSign:
            ds = DirAndSign[d]
            directions = ds[0]
            s = ds[1]
            for cab in selectedCells:
                ok = True
                for c in selectedCells:
                    row = (c[0]-cab[0])//s
                    col = (c[1]-cab[1])//s
                    if (row,col) not in directions:
                        ok = False
                        break
                if ok:
                    return cab,d
        raise PlaneError("Invalid plane!")

class PlaneError(Exception):
    """
    Exception class used in case there is an error related to a plane.
    """
    pass
