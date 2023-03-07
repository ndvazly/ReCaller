from AppGlobals import Globals
from tkinter import Frame
import tkinter as tk


class RevisionFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self['bg'] = Globals().DarkBG

        tk.Label(self, text='stripi').pack()
        # self.pack(fill=tk.Y, anchor=tk.NE)
