from tkinter import *
from PIL import ImageTk, Image

class imageResources:

    images = {}

    def getResizedImage(imgPath: str, size: tuple) -> PhotoImage:
        background_file = Image.open(imgPath)
        background_resized = background_file.resize((round(size[0]), round(size[1])), Image.ANTIALIAS)
        return ImageTk.PhotoImage(background_resized)

    def addImage(id: int, img: PhotoImage):
        imageResources.images[id] = img
        
