from tkinter.constants import SEPARATOR
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.messagebox as tkm
import background_board as bb
import stone as st
from statics import *

class GameManager:

    board: bb.BackgroundBoard
    gameLog:list = []
    whosTurn: int = BLACK
    stoneCount:int = 0
    __rootWnd: tk.Tk = None
    __canPlace = False

    def __init__(self, board: bb.BackgroundBoard, enableRenjuRule=True, rootWnd=None):
        self.board = board
        self.board.onStonePlace = self.whenClick
        self.resetGameLog()
        self.__enableRenjuRule = enableRenjuRule
        self.__rootWnd = rootWnd

    # Render board. This will erase every stone on the board.
    def renderBoard(self):
        self.board.drawBackground()

    # Reset (or initialize) gameLog.
    def resetGameLog(self):
        self.gameLog = []

        for _ in range(19):
            self.gameLog.append([BLANK for _ in range(19)])


    # Reset gameLog, re-render the board.
    def startGame(self):
        self.whosTurn = BLACK
        self.resetGameLog() 
        self.renderBoard()
        self.__canPlace = True
        self.stoneCount = 0
        self.setWndTitle(self.whosTurn)

    # Click event handler
    def whenClick(self, pos: tuple):

        # Ignore if place is occupied or __canPlace is False
        if self.gameLog[pos[0]][pos[1]] != BLANK or not self.__canPlace:
            return
        
        # Ignore if black stone cannot be placed according to renju rule, and show msgbox
        if self.whosTurn == BLACK and not self.__canblack(pos):
            tkm.showinfo(PROJECT_NAME, '렌주룰에 따라 흑은 여기에 둘 수 없습니다.')
            return

        # Render board, update gameLog, change window title, set stone count
        self.board.drawStone(st.Stone(self.board, pos, self.whosTurn))
        self.gameLog[pos[0]][pos[1]] = self.whosTurn
        self.stoneCount += 1
        self.setWndTitle(BLACK if self.whosTurn == WHITE else WHITE)

        # Check win/lose
        if self.__isit5(pos):
            self.__canPlace = False
            tkm.showinfo(PROJECT_NAME, '%s이 이겼습니다!\n확인을 누르면 초기화하고 다시 시작합니다.' % ('흑' if self.whosTurn == BLACK else '백'))
            self.startGame()
            return

        # Change turn
        self.whosTurn = BLACK if self.whosTurn == WHITE else WHITE


    # Set title name
    def setWndTitle(self, turn: int):
        turn = ('흑' if turn == BLACK else '백') + '차례'
        scount = str(self.stoneCount) + '수' if self.stoneCount != 0 else ''
        title = PROJECT_NAME + ' (%s'%turn + (')' if scount == '' else ' | %s)'%scount)
        self.__rootWnd.title(title)

    # Search stones around pos
    def __searchStones(self, pos: tuple) -> list:
        x, y = pos[0], pos[1]
        searchtmp = [] 
        type = self.gameLog[x][y]
        inrange = lambda x,y: 0<=x<=18 and 0<=y<=18

        for _ in range(4):
            searchtmp.append([BLANK for _ in range(9)])

        for i in range(-4,5):
            if inrange(x, y+i):
                searchtmp[0][4-i] = self.gameLog[x][y+i]
            if inrange(x+i, y):
                searchtmp[1][4-i] = self.gameLog[x+i][y]
            if inrange(x+i, y+i):
                searchtmp[2][4-i] = self.gameLog[x+i][y+i]
            if inrange(x-i, y+i):
                searchtmp[3][4-i] = self.gameLog[x-i][y+i]
        
        return searchtmp

    # Determinte win/lose
    def __isit5(self, pos: tuple) -> bool:

        # Search
        searchtmp = self.__searchStones(pos)
        type = self.gameLog[pos[0]][pos[1]]

        # Find 5 continuous stones
        for i in range(4):
            cont = 0

            for k in range(9):
                if searchtmp[i][k] == type:
                    cont += 1
                    if cont >= 5:
                        return True
                else:
                    cont = 0
            

        return False

    # Determine the position could be placed by black (renju rule)
    # forbid three cases: 33, 44, more than continuous 6
    def __canblack(self, pos:tuple) -> bool:

        # Declare forbids
        double3 = (BLANK, BLACK, BLACK, BLACK, BLANK)
        double4 = (BLANK, BLACK, BLACK, BLACK, BLACK, BLANK)

        # Declare loop escape variable
        done = False

        # Replace value temporarily
        pos_old = self.gameLog[pos[0]][pos[1]]
        self.gameLog[pos[0]][pos[1]] = BLACK

        # Find
        for line in range(19):
            if done:
                break
            for idx in range(19):

                # Check forbids only if position is already or is going to be black.
                if self.gameLog[line][idx] != BLACK and (line,idx) != pos:
                    continue

                # Declare forbid counts
                double3cnt, double4cnt, cont6cnt = 0, 0, 0

                # Search
                searchtmp = self.__searchStones((line, idx))

                for i in range(4):
                    double3cont, double4cont, cont = 0, 0, 0

                    for k in range(9):

                        # Find continuous 0,1,1,1,0 (33)
                        if searchtmp[i][k] == double3[double3cont]:
                            if double3cont == 4:
                                double3cnt += 1
                                double3cont = 1 if searchtmp[i][k] == double3[0] else 0
                            else:
                                double3cont += 1
                        else:
                            double3cont = 1 if searchtmp[i][k] == double3[0] else 0

                        # Find continuous 0,1,1,1,1,0 (44)
                        if searchtmp[i][k] == double4[double4cont]:
                            if double4cont == 5:
                                double4cnt += 1
                                double4cont = 1 if searchtmp[i][k] == double4[0] else 0
                            else:
                                double4cont += 1
                        else:
                            double4cont = 1 if searchtmp[i][k] == double4[0] else 0


                        # Find continous stones more than 6
                        if searchtmp[i][k] == BLACK:
                            cont += 1
                            if cont >= 6:
                                cont6cnt += 1 # One line can contain only one continuous 6. cont doesn't need to be reset.
                        else:
                            cont = 0


                if double3cnt > 1 or double4cnt > 1 or cont6cnt > 0:
                    done = True
                    break

        # Change value to original 
        self.gameLog[pos[0]][pos[1]] = pos_old

        # Finish
        return double3cnt < 2 and double4cnt < 2 and cont6cnt == 0
