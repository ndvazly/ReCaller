import tkinter as tk
from tkinter import Frame
from AppGlobals import Globals


class TopToolbar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self['bg'] = Globals().ToolbarBG

        # Add new channel strip button
        tk.Button(self, text='+', font=Globals().HeaderFont, bg=Globals().ButtonBG).grid(row=0,
                                                                                         column=self.grid_size()[0])
        tk.Button(self, text='p', font=Globals().HeaderFont, bg=Globals().ButtonBG,
                  command=self.parent.open_patchbays_window).grid(row=0, column=self.grid_size()[0])

        self.pack(fill=tk.X, anchor=tk.N)
