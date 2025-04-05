import tkinter

import model
import view
import controller

win = None


if __name__ == "__main__":
    running:bool = True
    ##model.init()
    root = tkinter.Tk()
    win = view.Window(root)
    ##controller.init()
    root.mainloop()
    