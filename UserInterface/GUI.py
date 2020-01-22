import PySimpleGUI
from domain.plane import PlaneValidator


class GUI:
    def __init__(self, planesService):
        self.__srv = planesService
        self.GUI = PySimpleGUI
        self.GUI.change_look_and_feel('DarkAmber')
        self.window = self.GUI.Window('Planes', self.theLayout(), resizable=True, element_justification='center')
        self.selectedCells = []
        self.addedPlanes = 0
        self.__hitRes = {'cabin': "{} DESTROYED a plane!", 'hit': "{} HIT a plane!", 'miss': "{} MISSED!"}

    def resetGame(self):
        self.__srv.resetGame()
        self.window.Close()
        self.window = self.GUI.Window('Planes', self.theLayout(), resizable=True, element_justification='center')
        self.selectedCells = []
        self.addedPlanes = 0

    def CBtn(self, button_text, i, j, b):
        return self.GUI.Button(button_text, pad=(0, 0), size=(2, 1), button_color=('white', 'light blue'),
                               key=(i, j, b))

    def theLayout(self):
        return [[self.GUI.Text('~   W E L C O M E   T O   P L A N E S   ~')]] + \
               [[self.GUI.Text(
                   "You must add 2 planes in your grid; plane width is 5 (wings), plane length is 4 (cabin-tail).\nClick 'Add plane' after each drown plane.",
                   key='Info', size=(50, 3))]] + \
               [[self.GUI.Text('Your planes: ', size=(25, 1)), self.GUI.Text('Your shots: ', size=(25, 1))]] + \
               [[self.CBtn('', i, j, 1) for j in range(8)] + [self.GUI.Text('  ')] + [self.CBtn('', i, j, 2) for j in
                                                                                      range(8)] for i in range(8)] + \
               [[self.GUI.Button('Add plane', pad=(0, 5), size=(9, 1)),
                 self.GUI.Text('{}'.format('~' * 40), pad=(2, 0))]] + \
               [[self.GUI.Quit('Quit game', pad=(0, 10), size=(9, 1)), self.GUI.Text('©  M. Ștefan C.', pad=(76, 10)),
                 self.GUI.Button('Reset game', pad=(0, 10), size=(9, 1))]]

    def updateCell(self, key):
        if self.addedPlanes == 2:
            raise Exception("You can't shoot your own planes!")
        cell = self.window[key]
        cellPos = (key[0], key[1])
        if cellPos in self.selectedCells:
            self.selectedCells.remove(cellPos)
            cell.Update(button_color=('white', 'light blue'))
        else:
            self.selectedCells.append(cellPos)
            cell.Update(button_color=('white', 'grey'))

    def addPlayerPlane(self):
        if self.addedPlanes >= 2:
            raise Exception('You already added 2 planes!')
        cabPos, orientation = PlaneValidator.GUIValidate(self.selectedCells)
        self.__srv.addPlayerPlane(cabPos, orientation)
        self.addedPlanes += 1
        color = 'green'
        if self.addedPlanes < 2:
            color = 'dark green'
        for c in self.selectedCells:
            cell = self.window[(c[0], c[1], 1)]
            cell.Update(button_color=('white', color))
        self.selectedCells.clear()
        if self.addedPlanes == 2:
            self.window['Info'].Update("The computer placed its planes as well.\nTry to hit them in the second grid!")

    def updateBoards(self):
        b1 = self.__srv.getPlayerBoard()
        b2 = self.__srv.getHitBoard()
        for i in range(8):
            for j in range(8):
                if b1[i][j] == 'X':
                    self.window[(i, j, 1)].Update(button_color=('red', 'red'))
                elif b1[i][j] == 0:
                    self.window[(i, j, 1)].Update(button_color=('red', 'blue'))
                if b2[i][j] == 'X':
                    self.window[(i, j, 2)].Update(button_color=('red', 'red'))
                elif b2[i][j] == 0:
                    self.window[(i, j, 2)].Update(button_color=('red', 'blue'))

    def showComputerPlanes(self):
        bc = self.__srv.getComputerBoard()
        for i in range(8):
            for j in range(8):
                if bc[i][j] == '#':
                    self.window[(i, j, 2)].Update(button_color=('red', 'pink'))

    def showHitResults(self, playerRes, computerRes):
        playInfo = "The computer placed its planes as well.\nTry to hit them in the second grid!\n"
        playerResultStr = self.__hitRes[playerRes].format('You')
        if computerRes is None:
            computerRes = ''
        else:
            computerRes = self.__hitRes[computerRes].format('Computer')
        self.window.Element('Info').Update("{}{}{}{}".format(playInfo, playerResultStr, ' ' * 10, computerRes))
        self.updateBoards()

    def shooting(self, key):
        if self.addedPlanes < 2:
            raise Exception("You have to add your 2 planes first!")
        if self.__srv.getWinner() is not None:
            raise Exception("This round has ended!\nPress 'Reset game' to start a new game.")
        # Player's turn
        hitRes1 = self.__srv.playerHit((key[0], key[1]))
        self.showHitResults(hitRes1, None)
        if self.__srv.getWinner() == 'human':
            self.GUI.Popup("YOU HAVE WON!", title='Winner')
            return
        # Computer's turn
        hitRes2 = self.__srv.computerHit()
        self.showHitResults(hitRes1, hitRes2)
        if self.__srv.getWinner() == 'computer':
            self.showComputerPlanes()
            self.GUI.Popup("GAME OVER! You have lost.", title='Winner')

    def run(self):
        while True:
            try:
                event, value = self.window.read()
                if event in ('Quit game', None):
                    self.window.Close()
                    break
                if event == 'Add plane':
                    self.addPlayerPlane()
                elif event == 'Reset game':
                    self.resetGame()
                elif event[2] == 1:
                    self.updateCell(event)
                else:
                    self.shooting(event)
            except Exception as ex:
                self.GUI.Popup(ex, title='Error')
