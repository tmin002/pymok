from tkinter import *
from PIL import ImageTk, Image

from background_board import * 
from game_manager import *
from resources import imageResources
from statics import *
from stone import *

def start():

    # Window setting
    windowSize: tuple = (800, 800) # Must be a square.
    boardPadding = 50
    rootWindow: Tk = Tk()
    rootWindow.size = windowSize 
    rootWindow.geometry("%dx%d" % (windowSize[0], windowSize[1])) #화면의 크기 설정
    rootWindow.resizable(width=False, height=False) #크기 조정은 불가능


    # Load background image
    imageResources.addImage(BACKGROUND_IMAGE, imageResources.getResizedImage(imgPath=BACKGROUND_IMAGE_PATH, size=windowSize))

    # Load widgets
    bgboard = BackgroundBoard(root=rootWindow, linePadding=boardPadding)
    bgboard.pack()

    # Create game manager
    gmanager = GameManager(board=bgboard, rootWnd=rootWindow)
    gmanager.startGame()

    # Load other images
    imageResources.addImage(STONE_BLACK_IMAGE, imageResources.getResizedImage(imgPath=STONE_BLACK_IMAGE_PATH, size=(bgboard.spaceBetweenLines, bgboard.spaceBetweenLines)))
    imageResources.addImage(STONE_WHITE_IMAGE, imageResources.getResizedImage(imgPath=STONE_WHITE_IMAGE_PATH, size=(bgboard.spaceBetweenLines, bgboard.spaceBetweenLines)))

    # Mainloop
    rootWindow.mainloop()

def intro():
    print('Application Programming Term Project <Team 14>')
    print('Project name: %s' % PROJECT_NAME)


# Run only if main.py is the first file read. 
# Does not run if main.py is imported. 
if __name__ == '__main__':
    intro()
    start()
