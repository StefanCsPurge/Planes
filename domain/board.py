from copy import deepcopy

class Board:
    def __init__(self,width,height,fillEl=' '):
        """
        Board object constructor.
        :param width: int - positive number
        :param height: int - positive number
        :param fillEl: one element to fill the board cells
        """
        self.__matrix = []
        for i in range(height):
            self.__matrix += [[fillEl]*width]

    def getMatrix(self):
        """
        Getter for the board matrix
        :return: list of lists - the board matrix
        """
        return deepcopy(self.__matrix)



