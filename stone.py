from PIL import ImageTk, Image
import tkinter as tk
import background_board as bb
import resources as r
from statics import *

class Stone:

    def getDrawInfo(board: bb.BackgroundBoard, position: tuple) -> dict:
        return \
            {
               "location": (int(board.padding + board.spaceBetweenLines*(position[0]-0.5)), int(board.padding + board.spaceBetweenLines*(position[1]-0.5))),
                "size": (int(board.spaceBetweenLines),int(board.spaceBetweenLines))
            }

    def __init__(self, root: bb.BackgroundBoard, position: tuple, type: int):

        # Initialize
        self.root = root
        self.position = position
        self.type = type
        self.root = root

    def draw(self):
        di = Stone.getDrawInfo(self.root, self.position)
        type = STONE_WHITE_IMAGE if self.type == WHITE else STONE_BLACK_IMAGE
        self.root.create_image(di['location'], anchor=tk.NW, image=r.imageResources.images[type])