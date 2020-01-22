from unittest import TestCase
from controllers.gameSrv import GameService
from domain.board import Board
from domain.plane import Plane,PlaneValidator,PlaneError

class TestComputerController(TestCase):
    def setUp(self):
        self.srv = GameService()

    def testResetGame(self):
        self.srv.getHitBoard()[0][0] = 0
        self.srv.resetGame()
        self.assertEqual(self.srv.getHitBoard(),Board(8,8).getMatrix())

    def testGetPlayerBoard(self):
        self.srv.resetGame()
        self.assertEqual(self.srv.getPlayerBoard(),Board(8,8).getMatrix())

    def testGetComputerBoard(self):
        self.srv.resetGame()
        self.assertEqual(type(self.srv.getComputerBoard()),type(Board(8,8).getMatrix()))

    def testGetHitBoard(self):
        self.srv.resetGame()
        self.assertEqual(self.srv.getHitBoard(),Board(8,8).getMatrix())

    def testAddPlayerPlane(self):
        self.srv.resetGame()
        self.srv.addPlayerPlane((2,0),'left')
        b = self.srv.getPlayerBoard()
        self.assertEqual(b[2][0],'#')

    def testAddComputerPlanes(self):
        self.srv.resetGame()
        # computer planes were added at the reset automatically
        b = self.srv.getComputerBoard()
        usedCells = 0
        for i in range(8):
            for j in range(8):
                usedCells += 1 if b[i][j] == '#' else 0
        self.assertEqual(usedCells,20)

    def testGetWinner(self):
        self.srv.resetGame()
        winner = self.srv.getWinner()
        self.assertEqual(winner,'computer')

    def testMarkDestroyedPlane(self):
        self.srv.resetGame()
        p = Plane((2,0),'left')
        self.srv.markDestroyedPlane(p,self.srv.getPlayerBoard())
        b = self.srv.getPlayerBoard()
        XCells = 0
        for i in range(8):
            for j in range(8):
                XCells += 1 if b[i][j] == 'X' else 0
        self.assertEqual(XCells, 10)

    def testPlayerHit(self):
        self.srv.resetGame()
        result = self.srv.playerHit((0,0))
        self.assertEqual(result,'miss')
        b = self.srv.getComputerBoard()
        usedCell = None
        for i in range(8):
            for j in range(8):
                if b[i][j] == '#':
                    usedCell = (i,j)
                    break
        result = self.srv.playerHit(usedCell)
        self.assertTrue(result in ('hit','cabin'))

    def testComputerHit(self):
        self.srv.resetGame()
        result = self.srv.computerHit()
        self.assertEqual(result,'miss')
        self.srv.addPlayerPlane((2,0),'left')
        self.srv.addPlayerPlane((4,7),'right')
        result = self.srv.computerHit()
        self.assertTrue(result in ('miss','hit','cabin'))


class TestPlane(TestCase):
    def testGetCabinPosition(self):
        p = Plane((0,2),'up')
        self.assertEqual(p.getCabinPosition(),(0,2))
        p = Plane((4,7),'right')
        self.assertEqual(p.getCabinPosition(),(4,7))

    def testGetPlaneOrientation(self):
        p = Plane((0, 2), 'up')
        self.assertEqual(p.getPlaneOrientation(), 'up')
        p = Plane((4, 7), 'right')
        self.assertEqual(p.getPlaneOrientation(), 'right')

    def testGetPlaneCells(self):
        p = Plane((2,0),'left')
        goodCells = [(2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (2, 2), (1, 3), (2, 3), (3, 3)]
        pCells = p.getPlaneCells()
        self.assertEqual(len(pCells),10)
        for c in goodCells:
            if c not in pCells:
                assert False

    def testPlaneValidation(self):
        from domain.board import Board
        p = Plane(0,'up')
        b = Board(8,8).getMatrix()
        with self.assertRaises(PlaneError):
            PlaneValidator.validate(p,b)
        p = Plane((2, 0),'left')
        self.assertIsNone(PlaneValidator.validate(p,b))
        p = Plane((0,-1),'down')
        with self.assertRaises(PlaneError):
            PlaneValidator.validate(p,b)
        p = Plane((2, 0), 'right')
        with self.assertRaises(PlaneError):
            PlaneValidator.validate(p,b)

class TestBoardCreation(TestCase):
    def testGetMatrix(self):
        matrix = Board(1,2,'0').getMatrix()
        self.assertEqual(matrix,[['0'],['0']])
        matrix = Board(3,2).getMatrix()
        self.assertEqual(matrix,[[' ',' ',' '],[' ',' ',' ']])
