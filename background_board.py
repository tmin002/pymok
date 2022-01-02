from tkinter.constants import W
from PIL import ImageTk, Image
import tkinter as tk
from resources import imageResources

from statics import *

class BackgroundBoard(tk.Canvas):

    def __init__(self, root: tk.Tk, onclick=None, linePadding=5):
        
        # Initialize
        tk.Canvas.__init__(self, root, width=root.size[0], height=root.size[1])
        self.backgroundSize = root.size
        self.padding = linePadding
        self.spaceBetweenLines = (root.size[0] - linePadding*2)/18
        self.onStonePlace = onclick

        # Load background image
        self.drawBackground()

        # Set event handler 
        self.bind("<Button-1>", self.clickEventHandler)

    # Draw image
    def drawImage(self, pos: tuple, image: tk.PhotoImage):
        self.create_image((round(pos[0]), round(pos[1])), anchor=tk.NW, image=image)

    # Draw background.
    def drawBackground(self):
        self.create_image((0,0), anchor=tk.NW, image=imageResources.images[BACKGROUND_IMAGE])
        #self.drawBoardLine()

    # Draw stone.
    def drawStone(self, stone):
        stone.draw()

    # Draw lines. (use when background is not for board background)
    def drawBoardLine(self):
        for x in range(19):
            xp = self.padding + self.spaceBetweenLines*x
            yp = self.padding + self.spaceBetweenLines*18
            self.create_line(xp, self.padding, xp, yp)

        for y in range(19):
            xp = self.padding + self.spaceBetweenLines*18
            yp = self.padding + self.spaceBetweenLines*y
            self.create_line(self.padding, yp, xp, yp)

    def clickEventHandler(self, event) -> tuple:
        xp, yp = event.x, event.y
        pos = lambda n: (self.padding + self.spaceBetweenLines * (n - BOARD_CLICK_BOX_SIZE/2), \
                         self.padding + self.spaceBetweenLines * (n + BOARD_CLICK_BOX_SIZE/2))
        outrange = lambda n: n < pos(0)[0] or n > pos(18)[1]

        if outrange(xp) or outrange(yp):
            return None

        x_count, y_count = 0, 0

        while (pos(0)[0] > xp or xp > pos(0)[1]) and not outrange(xp):
            x_count += 1
            xp = xp - self.spaceBetweenLines 

        while (pos(0)[0] > yp or yp > pos(0)[1]) and not outrange(yp):
            y_count += 1
            yp = yp - self.spaceBetweenLines 

        self.onStonePlace((x_count, y_count))
